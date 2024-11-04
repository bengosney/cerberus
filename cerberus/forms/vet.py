from django import forms

from ..models import Vet


class VetForm(forms.ModelForm):
    class Meta:
        model = Vet
        fields = [
            "name",
            "phone",
            "details",
        ]

        widgets = {
            "phone": forms.TextInput(attrs={"x-mask": "99999 999999", "x-data": ""}),
        }
