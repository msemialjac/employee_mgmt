from django.http import HttpResponse
from django.template import loader

from .models import Employee

from os import listdir
from os.path import isfile, join
from mailmerge import MailMerge


def index(request):
    mypath = 'employee/docx/'
    report_list = sorted([f for f in listdir(mypath) if isfile(join(mypath, f))])
    employee_list = Employee.objects.order_by('id')

    template = loader.get_template('employee/index.html')
    context = {
        "report_list": report_list,
        "employee_list": employee_list
    }

    if request.POST.get('mybtn'):
        report = request.POST.get('report')
        empid = request.POST.get('empid')
        emp = Employee.objects.get(id=empid)

        document = f"employee/docx/{report}"

        with MailMerge(document, 'w') as file:
            file.merge(
                first_name=emp.first_name,
                last_name=emp.last_name,
                oib=emp.oib,
                client=emp.gender.title(),
                date_birth=str(emp.date_birth.strftime("%d.%m.%Y.")),
                fax=str(emp.date_work.strftime("%d.%m.%Y.")),
                country=emp.nationality,
                address=emp.address,
                zip=emp.zip,
                city=emp.city,
                school=emp.last_school,
                vss=emp.edu_degree,
                iban=emp.iban,
                bank=emp.bank,
                swift=emp.swift,
                item=emp.item,
                reserve=emp.exp_years,
                substitute=emp.exp_months,
                salutation=emp.exp_days,
                blank="")
            file.write(f'employee/downloads/popunjen_{report}')
    return HttpResponse(template.render(context, request))


