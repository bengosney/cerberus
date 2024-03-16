# Standard Library
from calendar import MONDAY, Calendar, month_name
from collections import defaultdict, namedtuple
from collections.abc import Iterable
from datetime import date, datetime, time, timedelta

# Django
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import RedirectView, TemplateView

# Third Party
from dateutil.relativedelta import relativedelta

# Locals
from ..forms import BookingForm
from ..models import Booking
from .crud_views import CRUDViews, Crumb
from .transition_view import TransitionView

BookingGroup = namedtuple("BookingDay", ["date", "bookings"])


class BookingCRUD(CRUDViews):
    model = Booking
    form_class = BookingForm
    sortable_fields = ["pet__customer", "pet", "service", "start", "length"]


class BookingCalenderRedirect(RedirectView):
    pattern_name = "booking_calender_month"

    def get_redirect_url(self, *args, **kwargs):
        kwargs["year"] = datetime.now().year
        kwargs["month"] = datetime.now().month

        return super().get_redirect_url(*args, **kwargs)


class CalendarBreadCrumbs:
    def get_breadcrumbs(self, year: int, month: int | None = None, day: int | None = None) -> list[Crumb]:
        crumbs = [
            Crumb("Dashboard", reverse_lazy("dashboard")),
            Crumb("Bookings", reverse_lazy("booking_list")),
            Crumb(year, reverse_lazy("booking_calender_year", kwargs={"year": year})),
            Crumb(month_name[month], reverse_lazy("booking_calender_month", kwargs={"year": year, "month": month}))
            if month is not None
            else None,
            Crumb(day, reverse_lazy("booking_calender_day", kwargs={"year": year, "month": month, "day": day}))
            if day is not None
            else None,
        ]

        return list(filter(lambda crumb: crumb is not None, crumbs))


class BookingCalenderYear(TemplateView, CalendarBreadCrumbs):
    template_name = "cerberus/booking_calender_year.html"

    def get_context_data(self, year, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            date = datetime(year=year, month=1, day=1)
        except ValueError as e:
            raise Http404(f"year {year} not found") from e

        context["date"] = date
        context["prev_year"] = year - 1
        context["year"] = year
        context["next_year"] = year + 1
        context["today"] = date.today()
        context["months"] = list(enumerate(month_name))[1:]
        context["breadcrumbs"] = self.get_breadcrumbs(year)

        return context


class BookingCalenderMonth(TemplateView, CalendarBreadCrumbs):
    template_name = "cerberus/booking_calender_month.html"

    def grouped_bookings(self, start: date, end: date) -> dict[date, list[Booking]]:
        bookings = Booking.objects.filter(start__gte=start, end__lte=end).order_by("start")

        bookings_by_date: dict[date, list[Booking]] = defaultdict(list)
        for booking in bookings:
            bookings_by_date[booking.start.date()].append(booking)

        return bookings_by_date

    def organize_bookings(self, dates: list[date]) -> Iterable[BookingGroup]:
        bookings_by_date = self.grouped_bookings(dates[0], dates[-1])

        return [BookingGroup(date, bookings_by_date[date]) for date in dates]

    def get_context_data(self, year, month, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            date = datetime(year=year, month=month, day=1)
        except ValueError as e:
            raise Http404(f"month {month} not found") from e

        calendar = Calendar(MONDAY)

        context["date"] = date
        context["year"] = year
        context["month"] = month
        context["next_month"] = date + relativedelta(months=1)
        context["prev_month"] = date + relativedelta(months=-1)
        context["calendar"] = self.organize_bookings(list(calendar.itermonthdates(year, month)))
        context["today"] = date.today()
        context["days"] = calendar.iterweekdays()
        context["breadcrumbs"] = self.get_breadcrumbs(year, month)

        return context


class BookingCalenderDay(TemplateView, CalendarBreadCrumbs):
    template_name = "cerberus/booking_calender_day.html"

    @staticmethod
    def add_time(time: time, delta: timedelta) -> time:
        return (datetime.combine(date.today(), time) + delta).time()

    @classmethod
    def get_times(cls, start: time, end: time, step: timedelta) -> Iterable[time]:
        cur: time = start
        while cur < end:
            yield cur
            cur: time = cls.add_time(cur, step)

    def grouped_bookings(self, start: datetime, end: datetime) -> dict[time, list[Booking]]:
        bookings = Booking.objects.filter(start__gte=start, end__lte=end).order_by("start")

        bookings_by_date: dict[time, list[Booking]] = defaultdict(list)
        for booking in bookings:
            bookings_by_date[booking.start.time()].append(booking)

        return bookings_by_date

    def organize_bookings(self, times: list[datetime]) -> Iterable[BookingGroup]:
        bookings_by_date = self.grouped_bookings(times[0], times[-1])

        return [BookingGroup(t, bookings_by_date[t.time()]) for t in times]

    def get_context_data(self, year, month, day, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            date = datetime(year=year, month=month, day=day)
        except ValueError as e:
            raise Http404("date not found") from e

        step = 15
        start = 6
        end = 19
        steps = range(0, (end - start) * (60 // step))
        times: list[datetime] = [date + timedelta(hours=start, minutes=15 * i) for i in steps]

        context["date"] = date
        context["year"] = year
        context["month"] = month
        context["day"] = day
        context["booking_times"] = self.organize_bookings(times)
        context["breadcrumbs"] = self.get_breadcrumbs(year, month, day)

        return context


class BookingStateActions(TransitionView):
    model = Booking
    field = "state"
