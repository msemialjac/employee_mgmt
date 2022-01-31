from django.core.validators import RegexValidator
from django.db import models
from django.core.exceptions import ValidationError
from .data import *


# https://regos.hr/app/uploads/2018/07/KONTROLA-OIB-a.pdf - validacija oiba - Regos
# http://oib.itcentrala.com/oib-validator/
def validate_oib(oib):
    control = 10
    for num in oib[0:10]:
        control = (control + int(num)) % 10
        if control == 0:
            control += 10
        control *= 2
        control %= 11
    if (11 - control) == 10:
        return 0 == int(oib[10])
    else:
        return (11 - control) == int(oib[10])


# http://iban.isplate.info/iban-provjera.aspx - pravila validacije ibana;
# https://www.iban.hr/iban-checker - iban checker
def validate_iban(iban):
    iban = iban[4:] + iban[:4]
    iban = iban[:-4] + str(iban_letters[iban[-4].upper()]) + str(iban_letters[iban[-3].upper()]) + iban[-2:]
    iban = int(iban)
    return iban % 97 == 1


def calculate_work_time():
    pass


class Employee(models.Model):
    first_name = models.CharField(max_length=40, verbose_name='Ime')
    last_name = models.CharField(max_length=40, verbose_name='Prezime', )
    oib = models.CharField(verbose_name='OIB',
                           validators=[RegexValidator(regex='^\d{11}$',
                                                      message='Duljina polja je točno 11 znamenki, samo znamenke!!!',
                                                      code='nomatch')], max_length=11, default='')
    item = models.CharField(max_length=200, verbose_name='Oprema', default='')
    date_birth = models.DateField(verbose_name='Datum rođenja:')
    date_work = models.DateField(verbose_name='Datum početka rada:')
    gender = models.CharField(verbose_name='Spol:', max_length=1, default='',
                              validators=[RegexValidator(regex='^[mMžŽ]{1}$',
                                                         message='Samo M ili Ž su dozvoljene opcije.',
                                                         code='nomatch')], editable=True)
    address = models.CharField(verbose_name='Prebivalište', max_length=40, default='')
    zip = models.CharField(verbose_name='Poštanski broj', max_length=5, default='')
    city = models.CharField(verbose_name='Grad', max_length=40, default='')
    nationality = models.CharField(verbose_name='Državljanstvo', max_length=20, default='')
    edu_degree = models.CharField(verbose_name='Stručna sprema', max_length=15, default='')
    last_school = models.CharField(verbose_name='Zadnja završena škola', max_length=100, default='')
    iban = models.CharField(validators=[RegexValidator(regex='^[A-Za-z]{2}\d{19}$',
                                                       message='Duljina polja je točno 21 (2 velika slova (A-Z) + 19 '
                                                               'znamenki)!!!',
                                                       code='nomatch')],
                            verbose_name='IBAN', max_length=21, default='')
    bank = models.CharField(max_length=60, default='', verbose_name='Banka', null=True, editable=False)
    bank_country = models.CharField(max_length=120, default='', verbose_name='Zemlja banke', null=True, editable=False)
    swift = models.CharField(max_length=20, default='', verbose_name='Swift br.', null=True, editable=False)
    exp_years = models.CharField(verbose_name='Staž - godine', max_length=2,
                                 validators=[RegexValidator(regex='^\d{2}|\d{1}$',
                                                            message='Samo znamenke. Najmanje jedna znamenka',
                                                            code='nomatch')], editable=True, null=True)
    exp_months = models.CharField(verbose_name='Staž - mjeseci', max_length=2,
                                  validators=[RegexValidator(regex='^([01]{1}\d{1}|\d{1}){1}$',
                                                             message='Samo znamenke. Najmanje jedna znamenka.',
                                                             code='nomatch')], editable=True, null=True)
    exp_days = models.CharField(verbose_name='Staž - dani', max_length=3,
                                validators=[RegexValidator(regex='^(\d{3}|\d{2}|\d{1}){1}$',
                                                           message='Samo znamenke. Najmanje jedna znamenka.',
                                                           code='nomatch')], editable=True, null=True)

    def clean(self):
        errors = {}
        if not errors.get('oib') and self.oib.isdecimal() and len(self.oib) == 11 and not validate_oib(self.oib):
            errors['oib'] = ('Kontrolni broj je krivi. Neispravan OIB!\n ')
        if not errors.get('iban') and self.iban[2:].isdecimal() and len(self.iban) == 21 and not validate_iban(self.iban):
            errors['iban'] = ('Provjera kontrolnog broja neuspjela. Neispravan IBAN!\n ')
        if not errors.get('exp_days') and self.exp_days.isdecimal() and int(self.exp_days) > 364:
            errors['exp_days'] = ('Unesen je preveliki broj dana. Maksimalni broj dana je 364!\n ')
        if not errors.get('exp_months') and self.exp_months.isdecimal() and int(self.exp_months) > 11:
            errors['exp_months'] = ('Unesen je preveliki broj mjeseci. Maksimalni broj mjeseci je 11!\n ')
        if not errors.get('exp_years') and self.exp_years.isdecimal() and int(self.exp_years) > 50:
            errors['exp_years'] = ('Unesen je preveliki broj godina. Maksimalni broj godina je 50!\n ')
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if not self.bank or self.bank == 'Nepoznata banka':
            bank_num = str(self.iban)[4:11]
            if bank_num in bank_numbers.keys():
                self.bank = bank_numbers[bank_num][0]
                self.swift = bank_numbers[bank_num][1]
            else:
                self.bank = 'Nepoznata banka'
                self.swift = 'Nepoznati swift'

        if not self.bank_country or self.bank_country == 'Nepoznata zemlja':
            if self.iban[:2].upper() in country_codes.keys():
                print("printam se")
                self.bank_country = country_codes[self.iban[:2].upper()][0]
            else:
                self.bank_country = 'Nepoznata zemlja'

        super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    # def clean(self):
    #     errors = {}
    #     if not errors:
    #         if self.first_name[0] != 'M':
    #             errors['first_name'] = ('Prvo slovo nije "M".\n ')
    #     if not errors:
    #         if "Mario" not in self.first_name:
    #             errors['first_name'] = ('Ime nije Mario.\n ')
    #     if not errors.get('iban'):
    #         if len(self.first_name) != 5:
    #             errors['iban'] = ('Ime nema točno 5 slova!\n ')
    #     if errors:
    #         if self.first_name[0] != 'M' and errors['first_name'] != ('Prvo slovo nije "M".\n '):
    #             errors['first_name'] += ('Prvo slovo nije "M".\n ')
    #         if "Mario" not in self.first_name and errors['first_name'] != ('Ime nije Mario.\n '):
    #             errors['first_name'] += ('Ime nije Mario.\n ')
    #         if len(self.first_name) != 5 and errors['iban'] != ('Ime nema točno 5 slova!\n '):
    #             errors['iban'] += ('Ime nema točno 5 slova!\n ')
    #             raise ValidationError(errors)
    #
    #     if errors:
    #         raise ValidationError(errors)

# def validation_name(value):
# if "Mario" in value:
#     return value
# else:
#     raise ValidationError("Ime nije Mario")
