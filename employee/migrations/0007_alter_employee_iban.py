# Generated by Django 4.0.1 on 2022-01-25 11:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0006_remove_employee_oib2_alter_employee_iban_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='iban',
            field=models.CharField(default='', max_length=21, validators=[django.core.validators.RegexValidator(code='nomatch', message='Duljina polja je točno 21 (2 velika slova + 19 znamenki)!!!', regex='^[A-Z]{2}\\d{19}$')], verbose_name='IBAN'),
        ),
    ]