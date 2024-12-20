from django import forms

from ..fields import GroupedMultipleModelChoiceField
from ..models import Charge, Customer, Invoice
from ..utils import minimize_whitespace
from ..widgets import CheckboxTable, SingleMoneyWidget


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            "customer",
            "details",
            "due",
            "adjustment",
            "customer_name",
            "invoice_address",
            "send_notes",
        ]
        widgets = {
            "adjustment": SingleMoneyWidget(),
            "due": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, "instance", None)
        if instance and instance.pk:
            self.fields["customer"].disabled = True


class UninvoicedChargesForm(forms.Form):
    charges = GroupedMultipleModelChoiceField(
        queryset=Charge.objects.uninvoiced(),
        choices_groupby="customer",
        widget=CheckboxTable(["name", "amount", "booking.date"]),
    )


class CustomerUninvoicedChargesForm(forms.Form):
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        widget=forms.HiddenInput,
        required=True,
    )
    charges = forms.ModelMultipleChoiceField(
        queryset=Charge.objects.none(),
        widget=CheckboxTable(["name", "amount", "booking.date"]),
    )

    def __init__(self, *args, **kwargs):
        customer = kwargs.pop("customer", None)
        super().__init__(*args, **kwargs)

        if self.is_bound and (customer_id := self.data.get("customer", None)):
            self.set_customer(customer_id)
        elif isinstance(customer, Customer):
            self.set_customer(customer.pk)
        elif isinstance(customer, int):
            self.set_customer(customer)
        else:
            raise ValueError("No customer provided")

    def set_customer(self, customer_id: int | None) -> None:
        self.fields["customer"].initial = customer_id
        self.fields["charges"].queryset = Charge.objects.filter(  # type: ignore
            customer_id=customer_id,
            invoice__isnull=True,
        ).prefetch_related("booking")


class InvoiceSendForm(forms.Form):
    attributes = {"x-data": minimize_whitespace("""{ send: true }""")}

    send_email = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"x-model.boolean.fill": "send"}),
    )
    to = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={":class": "{ 'display-none': ! send }"}),
    )
    send_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={":class": "{ 'display-none': ! send }"}),
    )
