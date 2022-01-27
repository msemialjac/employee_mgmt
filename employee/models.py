from django.core.validators import RegexValidator
from django.db import models


class Employee(models.Model):
    first_name = models.CharField(max_length=40, verbose_name='Ime')
    last_name = models.CharField(max_length=40, verbose_name='Prezime')
    # oib = models.CharField(max_length=11, verbose_name='OIB')
    oib = models.CharField(verbose_name='OIB',
        validators=[RegexValidator(regex='^\d{11}$',
                                   message='Duljina polja je točno 11 znamenki!!!',
                                   code='nomatch')], max_length=11, default='')
    item = models.CharField(max_length=200, verbose_name='Oprema', default='')
    # 11. znamenka predstavlja kontrolni broj izračunat po „Modul 11, 10“ ISO 7064.
    date_birth = models.DateField(verbose_name='Datum rođenja:')
    address = models.CharField(verbose_name='Prebivalište', max_length=40, default='')
    zip = models.CharField(verbose_name='Poštanski broj', max_length=5, default='')
    city = models.CharField(verbose_name='Grad', max_length=40, default='')
    nationality = models.CharField(verbose_name='Državljanstvo', max_length=20, default='')
    edu_degree = models.CharField(verbose_name='Stručna sprema', max_length=15, default='')
    last_school = models.CharField(verbose_name='Zadnja završena škola', max_length=100, default='')
    iban = models.CharField(validators=[RegexValidator(regex='^[A-Za-z]{2}\d{19}$',
                                                       message='Duljina polja je točno 21 (2 velika slova + 19 znamenki)!!!',
                                                       code='nomatch')],
                            verbose_name='IBAN', max_length=21, default='')
    bank = models.CharField(max_length=60, default='', verbose_name="Banka", null=True, editable=False, )

    def bank_name_from_number(self, iban):
        bank_numbers = {
            "2402006": "ERSTE &STEIERMÄRKISCHE BANK d.d. Rijeka",
            "2390001": "HRVATSKA POŠTANSKA BANKA d.d. Zagreb",
            "2407000": "OTP BANKA d.d. Split",
            "2340009": "PRIVREDNA BANKA ZAGREB d.d. Zagreb",
            "2484008": "RAIFFEISENBANK AUSTRIA d.d. Zagreb",
            "2503007": "SBERBANK d.d. Zagreb",
            "2360000": "ZAGREBAČKA BANKA d.d. Zagreb",

        }
        if str(iban)[4:11] in bank_numbers.keys():
            self.bank = bank_numbers[str(iban)[4:11]]
            return self.bank
        else:
            self.bank = ''
            return self.bank

    def save(self, *args, **kwargs):
        if not self.bank:
            bank_numbers = {
                "2402006": "ERSTE &STEIERMÄRKISCHE BANK d.d. Rijeka",
                "2390001": "HRVATSKA POŠTANSKA BANKA d.d. Zagreb",
                "2407000": "OTP BANKA d.d. Split",
                "2340009": "PRIVREDNA BANKA ZAGREB d.d. Zagreb",
                "2484008": "RAIFFEISENBANK AUSTRIA d.d. Zagreb",
                "2503007": "SBERBANK d.d. Zagreb",
                "2360000": "ZAGREBAČKA BANKA d.d. Zagreb",

            }
            if str(self.iban)[4:11] in bank_numbers.keys():
                self.bank = bank_numbers[str(self.iban)[4:11]]
            else:
                self.bank = ''

        super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
