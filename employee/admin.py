from django.contrib import admin
from employee.models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    exclude = ('bank',)


admin.site.register(Employee)
