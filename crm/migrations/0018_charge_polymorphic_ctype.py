# Generated by Django 4.0.5 on 2022-06-27 06:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('crm', '0017_remove_charge_content_type_remove_charge_object_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='charge',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_%(app_label)s.%(class)s_set+', to='contenttypes.contenttype'),
        ),
    ]
