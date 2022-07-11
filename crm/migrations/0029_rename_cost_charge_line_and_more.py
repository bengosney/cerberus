# Generated by Django 4.0.5 on 2022-07-11 07:57

from decimal import Decimal
from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0028_alter_customer_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='charge',
            old_name='cost',
            new_name='line',
        ),
        migrations.RenameField(
            model_name='charge',
            old_name='cost_currency',
            new_name='line_currency',
        ),
        migrations.AddField(
            model_name='charge',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='adjustment',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), max_digits=14),
        ),
    ]
