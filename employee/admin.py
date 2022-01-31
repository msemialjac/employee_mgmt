from django.contrib import admin
from employee.models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    exclude = ('ank',)


admin.site.register(Employee)
