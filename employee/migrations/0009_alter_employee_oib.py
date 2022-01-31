# Generated by Django 4.0.1 on 2022-01-31 19:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0008_alter_employee_exp_months'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='oib',
            field=models.CharField(default='', max_length=11, validators=[django.core.validators.RegexValidator(code='nomatch', message='Duljina polja je točno 11 znamenki, samo znamenke!!!', regex='^\\d{11}$')], verbose_name='OIB'),
        ),
    ]