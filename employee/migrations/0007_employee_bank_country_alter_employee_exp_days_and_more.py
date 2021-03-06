# Generated by Django 4.0.1 on 2022-01-31 18:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0006_alter_employee_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='bank_country',
            field=models.CharField(default='', editable=False, max_length=120, null=True, verbose_name='Zemlja banke'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='exp_days',
            field=models.CharField(max_length=3, null=True, validators=[django.core.validators.RegexValidator(code='nomatch', message='Samo znamenke. Najmanje jedna znamenka.', regex='^(\\d{3}|\\d{2}|\\d{1}){1}$')], verbose_name='Staž - dani'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='iban',
            field=models.CharField(default='', max_length=21, validators=[django.core.validators.RegexValidator(code='nomatch', message='Duljina polja je točno 21 (2 velika slova (A-Z) + 19 znamenki)!!!', regex='^[A-Za-z]{2}\\d{19}$')], verbose_name='IBAN'),
        ),
    ]
