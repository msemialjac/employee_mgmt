from django.core.validators import RegexValidator
from django.db import models


class Employee(models.Model):
    first_name = models.CharField(max_length=40, verbose_name='Ime')
    last_name = models.CharField(max_length=40, verbose_name='Prezime')
    oib = models.CharField(verbose_name='OIB',
                           validators=[RegexValidator(regex='^\d{11}$',
                                                      message='Duljina polja je točno 11 znamenki!!!',
                                                      code='nomatch')], max_length=11, default='')
    item = models.CharField(max_length=200, verbose_name='Oprema', default='')
    # 11. znamenka predstavlja kontrolni broj izračunat po „Modul 11, 10“ ISO 7064.
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
                                                       message='Duljina polja je točno 21 (2 velika slova + 19 znamenki)!!!',
                                                       code='nomatch')],
                            verbose_name='IBAN', max_length=21, default='')
    bank = models.CharField(max_length=60, default='', verbose_name='Banka', null=True, editable=False)
    swift = models.CharField(max_length=20, default='', verbose_name='Swift br.', null=True, editable=False)
    exp_years = models.CharField(verbose_name='Staž - godine', max_length=2,
                                 validators=[RegexValidator(regex='^\\d{2}|\d{1}$',
                                                            message='Samo znamenke. Najmanje jedna znamenka',
                                                            code='nomatch')], editable=True, null=True)
    exp_months = models.CharField(verbose_name='Staž - mjesec', max_length=2,
                                  validators=[RegexValidator(regex='^\d{2}|\d{1}$',
                                                             message='amo znamenke. Najmanje jedna znamenka',
                                                             code='nomatch')], editable=True, null=True)
    exp_days = models.CharField(verbose_name='Staž - dani', max_length=3,
                                validators=[RegexValidator(regex='^\d{3}|\d{2}|\d{1}$',
                                                           message='Samo znamenke. Najmanje jedna znamenka',
                                                           code='nomatch')], editable=True, null=True)

    def save(self, *args, **kwargs):
        if not self.bank or self.bank == 'Nepoznata banka':
            bank_numbers = {
                "2500009": ["ADDIKO BANK d.d. Zagreb", "HAAB HR 22"],
                "2481000": ["AGRAM BANKA d.d. Zagreb", "KREZ HR 2X"],
                "4133006": ["BANKA KOVANICA d.d. Varaždin", "SKOV HR 22"],
                "2488001": ["BKS BANK AG, Glavna podružnica Hrvatska", "BFKK HR 22"],
                "2485003": ["CROATIA BANKA d.d. Zagreb", "CROA HR 2X"],
                "2402006": ["ERSTE &STEIERMÄRKISCHE BANK d.d. Rijeka", "ESBC HR 22"],
                "2493003": ["HRVATSKA BANKA ZA OBNOVU I RAZVITAK Zagreb", "HKBO HR 2X"],
                "1001005": ["HRVATSKA NARODNA BANKA", "NBHR HR 2D"],
                "2390001": ["HRVATSKA POŠTANSKA BANKA d.d. Zagreb", "HPBZ HR 2X"],
                "2492008": ["IMEX BANKA d.d. Split", "IMXX HR 22"],
                "2380006": ["ISTARSKA KREDITNA BANKA UMAG d.d. Umag", "ISKB HR 2X"],
                "2489004": ["J&T banka d.d. Varaždin", "VBVZ HR 22"],
                "2400008": ["KARLOVAČKA BANKA d.d. Karlovac", "KALC HR 2X"],
                "4124003": ["KENTBANK d.d. Zagreb", "KENB HR 22"],
                "2407000": ["OTP BANKA d.d. Split", "OTPV HR 2X"],
                "2408002": ["PARTNER BANKA d.d. Zagreb", "PAZG HR 2X"],
                "2386002": ["PODRAVSKA BANKA d.d. Koprivnica", "PDKC HR 2X"],
                "2340009": ["PRIVREDNA BANKA ZAGREB d.d. Zagreb", "PBZG HR 2X"],
                "2484008": ["RAIFFEISENBANK AUSTRIA d.d. Zagreb", "RZBH HR 2X"],
                "2403009": ["SAMOBORSKA BANKA d.d. Samobor", "SMBR HR 22"],
                "2503007": ["SBERBANK d.d. Zagreb", "VBCR HR 22"],
                "2412009": ["SLATINSKA BANKA d.d. Slatina", "SBSL HR 2X"],
                "2360000": ["ZAGREBAČKA BANKA d.d. Zagreb", "ZABA HR 2X"],
            }

            bank_num = str(self.iban)[4:11]

            if bank_num in bank_numbers.keys():
                self.bank = bank_numbers[bank_num][0]
                self.swift = bank_numbers[bank_num][1]
            else:
                self.bank = 'Nepoznata banka'
                self.swift = 'Nepoznati swift'

        super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
