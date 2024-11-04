from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

from ...models import Booking


class Command(BaseCommand):
    help = "Clean empty booking slots"

    def handle(self, *args, **options):
        self.stdout.write("Check for invalid bookings")

        for booking in Booking.objects.all():
            try:
                booking.check_valid()
            except ValidationError:
                self.stdout.write(f"Found invalid booking: {booking.id}")
