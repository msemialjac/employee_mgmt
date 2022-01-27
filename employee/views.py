# from __future__ import print_function
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from django.views import generic
from .forms import MyForm

from .models import Employee
from django.utils import timezone

from mailmerge import MailMerge
from datetime import date


# Create your views here.

REPORT_CHOICES = [
    '1. Ovlaštenje banci',
    '2. HZZ formular',
    '3. HZMO formular',
    '4. HZZO formular',
    '5. Ugovor',
    '6. Sporazum o opremi'
]

# def index(request):
#     if request.method == 'POST':
#         form = MyForm(request.POST)
#         if form.is_valid():
#             print("Hello")
#             template = loader.get_template('employee/index.html')
#             return HttpResponseRedirect('/admin/')
#     else:
#         form = MyForm
#     template = loader.get_template('employee/index.html')
#     context = {
#         'form': form
#     }
#    return HttpResponse(template.render(context, request))
#    return render(request, '/employee/', {'form': form})

template_1 = "WordMerge1.docx"
document = MailMerge(template_1)


def index(request):
    report_list = REPORT_CHOICES
    employee_list = Employee.objects.order_by('id')
    template = loader.get_template('employee/index.html')
    context = {
        "report_list": report_list,
        "employee_list": employee_list
    }

    if request.POST.get('mybtn'):
        print('Testiramo')
        report = request.POST.get('report')
        empid = request.POST.get('empid')
        emp = Employee.objects.get(id=empid)

        print(report, emp.last_name, emp.first_name, emp.last_school)

        with MailMerge(template_1, 'w') as file:
            file.merge(
                company=emp.last_name,
                client=emp.first_name)
            file.write('test-output.docx')

    return HttpResponse(template.render(context, request))


