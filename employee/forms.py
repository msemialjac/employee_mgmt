from django import forms
from .models import Employee

class MyForm(forms.Form):
    choices = forms.ChoiceField()