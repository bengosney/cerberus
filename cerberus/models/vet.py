# Django
from django.db import models
from django.urls import reverse

# Third Party
import reversion
from rules.contrib.models import RulesModel

# Locals
from .. import rules

# Locals
from ..fields import SqidsModelField as SqidsField


@reversion.register()
class Vet(RulesModel):
    # Fields
    name = models.CharField(max_length=255)
    phone = models.CharField(blank=True, default="", max_length=128)
    details = models.TextField(blank=True, default="")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    sqid = SqidsField(real_field_name="id")

    class Meta:
        ordering = ("name",)
        rules_permissions = {
            "view": rules.is_owner,
        }

    def __str__(self) -> str:
        return f"{self.name}"

    def get_absolute_url(self) -> str:
        return reverse("vet_detail", kwargs={"pk": self.pk})
