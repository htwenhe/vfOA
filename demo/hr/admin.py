from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(department)
class departmentAdmin(admin.ModelAdmin):
    pass

@admin.register(employee)
class employeeAdmin(admin.ModelAdmin):
    pass