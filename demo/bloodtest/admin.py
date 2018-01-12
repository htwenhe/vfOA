from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    pass

@admin.register(BloodTestProcess)
class BloodTestProcessAdmin(admin.ModelAdmin):
    pass