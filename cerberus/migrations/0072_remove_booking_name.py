# Generated by Django 5.0.3 on 2024-03-29 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cerberus", "0071_booking_cost_additional_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="booking",
            name="name",
        ),
    ]
