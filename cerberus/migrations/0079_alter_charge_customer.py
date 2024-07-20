# Generated by Django 5.0.6 on 2024-07-05 10:01

import django.db.models.deletion
from django.db import migrations, models

def remove_invalid_charges(apps, schema_editor):
    Charge = apps.get_model("cerberus", "Charge")
    Charge.objects.filter(customer_id__isnull=True).delete()
    Customer = apps.get_model("cerberus", "Customer")
    for charge in Charge.objects.all():
        if not Customer.objects.filter(id=charge.customer_id).exists():
            charge.delete()

class Migration(migrations.Migration):

    dependencies = [
        ("cerberus", "0078_auto_20240425_0726"),
    ]

    operations = [
        migrations.RunPython(remove_invalid_charges),
        migrations.AlterField(
            model_name="charge",
            name="customer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="charges",
                to="cerberus.customer",
            ),
        ),
    ]
