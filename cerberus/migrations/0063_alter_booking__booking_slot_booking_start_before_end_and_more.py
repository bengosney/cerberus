# Generated by Django 5.0.3 on 2024-03-23 18:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cerberus", "0062_alter_booking_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="_booking_slot",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="bookings",
                to="cerberus.bookingslot",
            ),
        ),
        migrations.AddConstraint(
            model_name="booking",
            constraint=models.CheckConstraint(
                check=models.Q(("start__lt", models.F("end"))), name="start_before_end"
            ),
        ),
        migrations.AddConstraint(
            model_name="booking",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(
                        models.Q(("state", "canceled"), _negated=True),
                        ("_booking_slot__isnull", False),
                    ),
                    models.Q(("state", "canceled"), ("_booking_slot__isnull", True)),
                    _connector="OR",
                ),
                name="has_booking_slot",
            ),
        ),
    ]