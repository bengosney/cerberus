from collections import Counter

from django.core.management.base import BaseCommand

from ...exceptions import InvalidEmailError
from ...models import Contact, Customer


class Command(BaseCommand):
    help = "Fix bad customer data"

    def handle(self, *args, **options):
        self.stdout.write("Fixing as many customers it can")

        for customer in Customer.objects.all():
            if customer.invoice_email == "":
                counts = Counter([c.type for c in customer.contacts.all()])
                if counts[Contact.Type.EMAIL] == 1:
                    self.stdout.write(f"Can fix invoice email for {customer.name}")
                    for contact in customer.contacts.all():
                        try:
                            contact.set_as_invoice()
                        except InvalidEmailError:
                            pass
