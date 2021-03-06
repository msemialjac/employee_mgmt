# Generated by Django 4.0.1 on 2022-01-31 08:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='exp_days',
            field=models.CharField(max_length=3, null=True, validators=[django.core.validators.RegexValidator(code='nomatch', message='Samo znamenke. Najmanje jedna znamenka. Max 365 dana', regex='^[0-3]{1}\\d{2}|\\d{2}|\\d{1}$')], verbose_name='Staž - dani'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='exp_months',
            field=models.CharField(max_length=2, null=True, validators=[django.core.validators.RegexValidator(code='nomatch', message='Samo znamenke. Najmanje jedna znamenka. Max 11 mjeseci', regex='^[0-1]{1}\\d{1}|\\d{1}$')], verbose_name='Staž - mjeseci'),
        ),
    ]
