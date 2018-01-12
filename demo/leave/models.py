from django.db import models
from viewflow.models import Process
from demo.hr.models import *


class Leave_class(models.Model):
    name= models.CharField(max_length=256, verbose_name=u"名称")
    class Meta:
        db_table = 'leave_class'
        verbose_name = '请假类别'
        verbose_name_plural = "请假类别"



    def __str__(self):
        return self.name


# class department(models.Model):
#     name = models.CharField(max_length=256, verbose_name=u"名称")
#     leader = models.ForeignKey(User, verbose_name=u"部门经理")
#
#     class Meta:
#         db_table = 'department'
#         verbose_name = '部门'
#         verbose_name_plural = "部门"
#
#     def __str__(self):
#         return self.name

class Leave(models.Model):
    """请假内容"""
    req_by = models.ForeignKey(employee, verbose_name=u"申请人")
    req_date = models.DateTimeField(verbose_name=u"申请时间")
    depart_name = models.ForeignKey(department,verbose_name=u'部门')
    position =  models.CharField(max_length=256,  verbose_name=u"职位")
    req_class =models.ForeignKey(Leave_class,verbose_name=u'请假类别')
    start_time=models.DateTimeField(verbose_name=u"开始时间")
    end_time=models.DateTimeField(verbose_name=u"结束时间")
    resion=models.CharField(max_length=256,  verbose_name=u"请假事由")
    file_url=models.CharField(max_length=256,  verbose_name=u"上传附件")
    comment = models.CharField(max_length=256, verbose_name=u"备注",blank=True,null=True)
    #审批领导

    class Meta:
        db_table = 'leave'
        verbose_name = '请假'
        verbose_name_plural = "请假"

    def __str__(self):
        return self.req_by.user.username


class LeaveProcess(Process):

    leave = models.OneToOneField(Leave,null=True,blank=True)

    dep_approved = models.IntegerField(default=0, verbose_name=u"部门审核")
    dep_approved_time = models.DateTimeField(verbose_name=u"部门领导审核时间",blank=True,null=True)
    dep_approved_comment = models.CharField(max_length=256, verbose_name=u"部门领导审核意见",blank=True,null=True)

    hr_approved = models.IntegerField(default=0, verbose_name=u"人事审核")
    hr_approved_time = models.DateTimeField(verbose_name=u"人事审核时间",blank=True,null=True)
    hr_approved_comment= models.CharField(max_length=256, verbose_name=u"人事审核意见",blank=True,null=True)
    comment=models.CharField(max_length=1024,blank=True,null=True)

    class Meta:
        db_table = 'leave_process'
        verbose_name = '请假过程'
        verbose_name_plural = "请假过程"
