# Generated by Django 5.0.4 on 2024-04-16 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cerberus", "0075_alter_pet_tags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pet",
            name="neutered",
            field=models.CharField(
                blank=True,
                choices=[
                    (None, "(Unknown)"),
                    ("yes", "Yes"),
                    ("no", "No"),
                    ("implant", "Implant"),
                ],
                db_default="(Unknown)",
                default="(Unknown)",
                max_length=7,
            ),
        ),
        migrations.AlterField(
            model_name="pet",
            name="sex",
            field=models.CharField(
                blank=True,
                choices=[(None, "(Unknown)"), ("male", "Male"), ("female", "Female")],
                db_default="(Unknown)",
                default="(Unknown)",
                max_length=6,
            ),
        ),
    ]
