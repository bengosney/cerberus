# Standard Library
from collections.abc import Callable, Iterable
from datetime import date, datetime, timedelta
from functools import reduce
from operator import or_
from typing import TYPE_CHECKING, Self

# Django
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import CheckConstraint, F, Max, Min, Q
from django.db.models.query import QuerySet
from django.urls import reverse

# Third Party
import reversion
from django_fsm import FSMField, Transition, transition
from djmoney.models.fields import MoneyField
from humanize import naturaldate

# Locals
from ..decorators import save_after
from ..exceptions import IncorectServiceError, MaxCustomersError, MaxPetsError, SlotOverlapsError
from ..utils import make_aware
from .charge import Charge
from .service import Service

if TYPE_CHECKING:
    # Locals
    from . import Customer, Pet, Service


class BookingSlot(models.Model):
    id: int
    bookings: models.QuerySet["Booking"]

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    start = models.DateTimeField()
    end = models.DateTimeField()
    length = models.GeneratedField(  # type: ignore
        expression=F("end") - F("start"),
        output_field=models.DurationField(),
        db_persist=True,
    )

    class Meta:
        unique_together = [("start", "end")]
        constraints = [CheckConstraint(check=Q(start__lt=F("end")), name="slot_start_before_end")]

    def __str__(self) -> str:
        return f"{self.id}: {self.start} - {self.end}"

    @classmethod
    def get_slot(cls, start: datetime, end: datetime) -> Self:
        try:
            slot = cls.objects.get(start=start, end=end)
        except cls.DoesNotExist:
            slot = cls(start=start, end=end)
            slot.save()

        return slot

    @staticmethod
    def round_date_time(dt: datetime) -> datetime:
        dt = dt - timedelta(minutes=dt.minute % 10, seconds=dt.second, microseconds=dt.microsecond)

        return make_aware(dt)

    def get_overlapping(self) -> QuerySet[Self]:
        start = Q(start__lt=self.start, end__gt=self.start)
        end = Q(start__lt=self.end, end__gt=self.end)
        equal = Q(start=self.start, end=self.end)
        contains = Q(start__gt=self.start, end__lt=self.end)

        return self.__class__.objects.filter(start | end | equal | contains).exclude(pk=self.pk)

    def overlaps(self) -> bool:
        others = self.get_overlapping()

        return any(o.bookings.all().count() > 0 for o in others)

    def clean(self) -> None:
        if self.overlaps():
            raise ValidationError(f"{self.__class__.__name__} overlaps another {self.__class__.__name__}")

        if len({booking.service.id for booking in self.bookings.all()}) > 1:
            raise ValidationError(f"{self.__class__.__name__} has multiple services")

        if (max_pet := getattr(self.service, "max_pet")) and self.pet_count > max_pet:
            raise ValidationError(f"{self.__class__.__name__} has max pets for service, {max_pet}")

        if (max_customer := getattr(self.service, "max_customer")) and self.customer_count > max_customer:
            raise ValidationError(f"{self.__class__.__name__} has max customers for service, {max_customer}")

        super().clean()

    def move_slot(self, start: datetime | date, end: datetime | None = None) -> bool:
        if not all(b.can_move for b in self.bookings.all()):
            return False

        if not isinstance(start, datetime):
            start = make_aware(
                datetime(start.year, start.month, start.day, self.start.hour, self.start.minute, self.start.second)
            )

        self.end = start + (self.end - self.start) if end is None else end
        self.start = start

        overlaps = self.get_overlapping()
        if overlaps.count():
            if overlaps.count() > 1:
                raise SlotOverlapsError("Slot overlaps multiple slots")

            if (overlapping := overlaps.first()) and self.matches(overlapping):
                overlapping += self
                return True

            raise SlotOverlapsError("Slot overlaps another")

        with transaction.atomic():
            self.save()
            for booking in self.bookings.all():
                booking.start = self.start
                booking.end = self.end
                booking.save()

        return True

    def contains_all(self, booking_ids: list[int]) -> bool:
        ids = [b.id for b in self.bookings.all()]
        return all(id in ids for id in booking_ids)

    def length_seconds(self) -> int:
        return int(self.length.total_seconds())

    def length_minutes(self) -> int:
        return self.length_seconds() // 60

    def matches(self, other: Self) -> bool:
        return self.start == other.start and self.end == other.end and self.service == other.service

    @classmethod
    def clean_empty_slots(cls) -> None:
        cls.objects.filter(bookings__isnull=True).delete()

    @property
    def service(self) -> "Service | None":
        try:
            return self.bookings.all()[0].service
        except IndexError:
            return None

    @property
    def pets(self) -> set["Pet"]:
        return {b.pet for b in self.bookings.all()}

    @property
    def pet_count(self) -> int:
        return len(self.pets)

    @property
    def customers(self) -> set["Customer"]:
        return {b.pet.customer for b in self.bookings.all()}

    @property
    def customer_count(self) -> int:
        return len(self.customers)

    def __add__(self, other: "Self|Booking") -> Self:
        if isinstance(other, Booking):
            with transaction.atomic():
                other.booking_slot = self
                other.start = self.start
                other.end = self.end
                other.save()
            return self

        if isinstance(other, self.__class__):
            if not self.matches(other):
                raise ValueError("Slots do not match")

            with transaction.atomic():
                for booking in other.bookings.all():
                    booking.move_booking(self.start)
                    booking.save()
            return self

        raise ValueError("Invalid type")


class BookingStates(models.TextChoices):
    ENQUIRY = "enquiry"
    PRELIMINARY = "preliminary"
    CONFIRMED = "confirmed"
    CANCELED = "canceled"
    COMPLETED = "completed"

    @classmethod
    def to_constraints(cls, field: str) -> Q:
        return reduce(or_, [Q(**{field: e.value}) for e in cls])


class ActiveBookingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(state=BookingStates.CANCELED.value)


@reversion.register()
class Booking(models.Model):
    STATES_MOVEABLE: list[str] = [
        BookingStates.ENQUIRY.value,
        BookingStates.PRELIMINARY.value,
        BookingStates.CONFIRMED.value,
    ]
    STATES_CANCELABLE: list[str] = [
        BookingStates.ENQUIRY.value,
        BookingStates.PRELIMINARY.value,
        BookingStates.CONFIRMED.value,
    ]

    id: int
    get_all_state_transitions: Callable[[], Iterable[Transition]]
    get_available_state_transitions: Callable[[], Iterable[Transition]]

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    name = models.CharField(max_length=520)
    cost = MoneyField(max_digits=14, default=0.0)
    start = models.DateTimeField()
    end = models.DateTimeField()
    length = models.GeneratedField(  # type: ignore
        expression=F("end") - F("start"),
        output_field=models.DurationField(),
        db_persist=True,
    )

    state = FSMField(default=BookingStates.PRELIMINARY.value, choices=BookingStates.choices, protected=True)  # type: ignore

    # Relationship Fields
    customer = models.ForeignKey("cerberus.Customer", on_delete=models.PROTECT, related_name="bookings")
    pets = models.ManyToManyField("cerberus.Pet", related_name="bookings")
    service = models.ForeignKey("cerberus.Service", on_delete=models.PROTECT, related_name="bookings")
    _booking_slot = models.ForeignKey(
        "cerberus.BookingSlot", on_delete=models.PROTECT, related_name="bookings", null=True, blank=True
    )
    _booking_slot_id: int | None
    _previous_slot: BookingSlot | None = None

    charges = GenericRelation(Charge)

    objects = models.Manager()
    active = ActiveBookingManager()

    class Meta:
        ordering = ("-created",)
        unique_together = [("customer", "_booking_slot")]
        constraints = [
            CheckConstraint(check=Q(start__lt=F("end")), name="start_before_end"),
            CheckConstraint(
                check=(~Q(state=BookingStates.CANCELED.value) & Q(_booking_slot__isnull=False))
                | (Q(state=BookingStates.CANCELED.value) & Q(_booking_slot__isnull=True)),
                name="has_booking_slot",
            ),
            CheckConstraint(check=BookingStates.to_constraints("state"), name="valid_state"),
        ]

    def __str__(self) -> str:
        return f"{self.name} - {naturaldate(self.start)}"

    def save(self, *args, **kwargs) -> None:
        self.name = f"{self.customer.name}, {self.service.name}"

        with transaction.atomic():
            if self.pk is None and getattr(self, "_booking_slot", None) is None:
                self._booking_slot = self._get_new_booking_slot()

            if self._booking_slot is not None:
                self._booking_slot.save()

            super().save(*args, **kwargs)

            if self._previous_slot is not None and self._previous_slot.pk and self._previous_slot.bookings.count() == 0:
                self._previous_slot.delete()

    def get_absolute_url(self):
        return reverse("booking_detail", kwargs={"pk": self.pk})

    @classmethod
    def get_mix_max_time(cls, date: date) -> tuple[datetime | None, datetime | None]:
        date = make_aware(datetime(date.year, date.month, date.day))
        next_date = date + timedelta(days=1)

        result = (
            cls.objects.filter(start__gt=date, end__lt=next_date).values("start").aggregate(Min("start"), Max("end"))
        )

        return result["start__min"], result["end__max"]

    @property
    def booking_slot(self) -> BookingSlot:
        if self._booking_slot is None:
            if self.state == BookingStates.CANCELED.value:
                raise (BookingSlot.DoesNotExist("Booking has been canceled"))
            self._booking_slot = self._get_new_booking_slot()
        return self._booking_slot

    @booking_slot.setter
    def booking_slot(self, value: BookingSlot) -> None:
        if value != self._booking_slot:
            self._previous_slot = self._booking_slot

        self._booking_slot = value

    def create_charge(self) -> Charge:
        charge = BookingCharge(
            name=f"Charge for {self.name}"[:255],
            line=self.cost,
            booking=self,
            customer=self.customer,
        )
        charge.save()

        return charge

    def _get_new_booking_slot(self) -> BookingSlot:
        slot = BookingSlot.get_slot(self.start, self.end)

        if slot.service != self.service and slot.service is not None:
            raise IncorectServiceError("Booking is for a different service")

        if slot.pet_count >= self.service.max_pet:
            raise MaxPetsError(f"Booking has max pets for service, {self.service.max_pet}")

        if slot.customer_count >= self.service.max_customer and self.pet.customer not in slot.customers:
            raise MaxCustomersError(f"Booking has max customers for service, {self.service.max_customer}")

        if slot.overlaps():
            overlaps = slot.get_overlapping()

            if not all(all(b.id == self.id for b in o.bookings.all()) for o in overlaps):
                raise SlotOverlapsError("Booking overlaps another")

        return slot

    @property
    def can_move(self) -> bool:
        return self.state in self.STATES_MOVEABLE

    def can_complete(self) -> bool:
        return self.end < make_aware(datetime.now())

    def move_booking(self, to: datetime | date) -> bool:
        if not self.can_move:
            return False

        if not isinstance(to, datetime):
            to = make_aware(datetime(to.year, to.month, to.day, self.start.hour, self.start.minute, self.start.second))

        delta = self.start - to
        self.start -= delta
        self.end -= delta

        self.booking_slot = self._get_new_booking_slot()
        self.save()

        return True

    def move_booking_slot(self, start: datetime | date) -> bool:
        if slot := self._booking_slot:
            if not isinstance(start, datetime):
                start = make_aware(
                    datetime(start.year, start.month, start.day, self.start.hour, self.start.minute, self.start.second)
                )

            length = slot.end - slot.start
            return slot.move_slot(start, start + length)

        return False

    def length_seconds(self) -> int:
        return int(self.length.total_seconds())

    def length_minutes(self) -> int:
        return self.length_seconds() // 60

    @save_after
    @transition(field=state, source=BookingStates.ENQUIRY.value, target=BookingStates.PRELIMINARY.value)
    def process(self) -> None:
        pass

    @save_after
    @transition(field=state, source=BookingStates.PRELIMINARY.value, target=BookingStates.CONFIRMED.value)
    def confirm(self) -> None:
        pass

    @save_after
    @transition(field=state, source=STATES_CANCELABLE, target=BookingStates.CANCELED.value)  # type: ignore
    def cancel(self) -> None:
        self._booking_slot = None

    @save_after
    @transition(field=state, source=BookingStates.CANCELED.value, target=BookingStates.ENQUIRY.value)
    def reopen(self) -> None:
        self._booking_slot = self._get_new_booking_slot()

    @save_after
    @transition(
        field=state,
        source=BookingStates.CONFIRMED.value,
        target=BookingStates.COMPLETED.value,
        conditions=[can_complete],
    )
    def complete(self) -> Charge:
        return self.create_charge()

    @property
    def available_state_transitions(self) -> list[str]:
        return [i.name for i in self.get_available_state_transitions()]


class BookingCharge(Charge):
    booking = models.ForeignKey(Booking, on_delete=models.PROTECT)
