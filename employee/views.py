from django.http import HttpResponse
from django.template import loader

from .models import Employee

from mailmerge import MailMerge

REPORT_CHOICES = [
    '1. Ovlaštenje banci',
    '2. HZZ formular',
    '3. HZMO formular',
    '4. HZZO formular',
    '5. Ugovor',
    '6. Sporazum o opremi'
]

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
        report = request.POST.get('report')
        empid = request.POST.get('empid')
        emp = Employee.objects.get(id=empid)

        with MailMerge(template_1, 'w') as file:
            file.merge(
                company=emp.last_name,
                client=emp.first_name)
            file.write('employee/downloads/obrazac_1_output.docx')

    return HttpResponse(template.render(context, request))


