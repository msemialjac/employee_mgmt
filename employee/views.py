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
        print(emp.first_name, 'drugo')
        print(report)
        document = f"employee/docx/{report}"

        with MailMerge(document, 'w') as file:
            file.merge(
                first_name=emp.first_name.title(),
                last_name=emp.last_name.title(),
                oib=emp.oib,
                gender=emp.gender.upper(),
                date_birth=str(emp.date_birth.strftime("%d.%m.%Y.")),
                date_work=str(emp.date_work.strftime("%d.%m.%Y.")),
                nationality=emp.nationality.capitalize(),
                address=emp.address,
                zip=emp.zip,
                city=emp.city.title(),
                school=emp.last_school,
                edu_degree=emp.edu_degree.upper(),
                iban=emp.iban.upper(),
                bank=emp.bank,
                swift=emp.swift,
                item=emp.item,
                exp_years=emp.exp_years,
                exp_months=emp.exp_months,
                exp_days=emp.exp_days,
                blank="")
            file.write(f'employee/downloads/{emp.first_name}_{emp.last_name}_{report}')
    return HttpResponse(template.render(context, request))


