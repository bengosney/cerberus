# Generated by Django 5.0.3 on 2024-03-25 08:43

import djmoney.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cerberus", "0065_booking_valid_state"),
    ]

    operations = [
        migrations.AlterField(
            model_name="service",
            name="cost_per_additional",
            field=djmoney.models.fields.MoneyField(
                blank=True, decimal_places=2, default=None, max_digits=14, null=True
            ),
        ),
        migrations.AlterField(
            model_name="service",
            name="cost_per_additional_currency",
            field=djmoney.models.fields.CurrencyField(
                choices=[("GBP", "GBP £")],
                default="GBP",
                editable=False,
                max_length=3,
                null=True,
            ),
        ),
    ]
