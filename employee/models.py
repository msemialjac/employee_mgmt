import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.core.validators import RegexValidator


# Create your models here.
class Employee(models.Model):
    name = models.CharField(name='Ime', max_length=40)
    last_name = models.CharField(name='Prezime:', max_length=40)
    oib = models.CharField(validators=[RegexValidator(regex='^\d{11}$', message='Duljina polja je točno 11 znamenki!!!', code='nomatch')])
    # 11. znamenka predstavlja kontrolni broj izračunat po „Modul 11, 10“ ISO 7064.
    date_birth = models.DateTimeField(verbose_name='Datum rođenja:')

    # @admin.display(
    #     boolean=True,
    #     ordering='pub_date',
    #     description='Published recently?',
    #     )

    # def was_published_recently(self):
    #     now = timezone.now()
    #     return now - datetime.timedelta(days=1) <= self.pub_date <= now
    def __str__(self):
        return f'{self.employee.name} {self.employee.last_name} '


# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=2)
#     votes = models.IntegerField(default=0)
#
#     def __str__(self):
#         return self.choice_text
