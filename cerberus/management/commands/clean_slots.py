# Standard Library
from contextlib import suppress

# Django
from django.core.management.base import BaseCommand
from django.db.models import ProtectedError

# First Party
from cerberus.models import BookingSlot


class Command(BaseCommand):
    help = "Clean empty booking slots"

    def handle(self, *args, **options):
        self.stdout.write("Removing empty booking slots")

        with suppress(ProtectedError):
            for slot in BookingSlot.objects.all():
                slot.delete()
                self.stdout.write("Removed slot")
