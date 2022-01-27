from django.contrib import admin
from employee.models import Employee


# Register your models here.
# class EmployeeAdmin(admin.ModelAdmin):
#     fields = ('first_name', 'last_name', 'oib')


class EmployeeAdmin(admin.ModelAdmin):
    exclude = ('bank',)


admin.site.register(Employee)
