# Generated by Django 4.2.2 on 2023-06-30 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("cerberus", "0050_auto_20230630_0714"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="customer",
            field=models.ForeignKey(
                default=0, on_delete=django.db.models.deletion.PROTECT, related_name="payments", to="cerberus.customer"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="payment",
            name="invoice",
            field=models.ForeignKey(
                limit_choices_to={"state": "unpaid"},
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="payments",
                to="cerberus.invoice",
            ),
        ),
        migrations.AddConstraint(
            model_name="payment",
            constraint=models.CheckConstraint(check=models.Q(("amount__gte", 0)), name="cerberus_payment_gte_0"),
        ),
    ]
