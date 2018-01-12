from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('req_by', 'req_date', 'resion')
    list_filter = ('req_by','depart_name','req_class')
    search_fields = ('resion',)

@admin.register(LeaveProcess)
class LeaveProcessAdmin(admin.ModelAdmin):
    list_display = ('req_by','req_date', 'resion', 'dep_approved', 'hr_approved')
    def req_by(self, LeaveProcess):
        return LeaveProcess.leave.req_by
    def req_date(self, LeaveProcess):
        return LeaveProcess.leave.req_date
    def resion(self, LeaveProcess):
        return LeaveProcess.leave.resion

@admin.register(Leave_class)
class Leave_classAdmin(admin.ModelAdmin):
    pass