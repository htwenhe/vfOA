from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(cs_process)
class CSAdmin(admin.ModelAdmin):
    list_display = ( 'version', 'mark')