# Generated by Django 4.0.1 on 2022-01-25 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0008_alter_employee_iban'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='name',
            new_name='first_name',
        ),
    ]
