from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class employee(models.Model):

    birthday =  models.DateTimeField(verbose_name=u"Date of Birth")
    passport_id = models.CharField(verbose_name=u'passport No',max_length=1024)
    sex = models.CharField(
        max_length=1,
        choices=(
            ("M", "Male"),
            ("F", "Female"),
            ("O", "Other")))
    marital= models.CharField(
        max_length=10,
        choices=(('single', 'Single'), ('married', 'Married'), ('widower', 'Widower'), ('divorced', 'Divorced')))
    department= models.ForeignKey('hr.department',related_name='member')
    address=models.CharField(verbose_name=u'Working Address',max_length=1024)
    work_phone= models.CharField(verbose_name=u'Work Phone',max_length=1024)
    mobile_phone= models.CharField(verbose_name=u'Work Mobile',max_length=1024)
    work_email= models.CharField(verbose_name=u'Work Email',max_length=1024)
    work_location= models.CharField(verbose_name=u'Office Location',max_length=1024)
    notes= models.CharField(verbose_name=u'Notes',max_length=1024)
    Manager=models.ForeignKey('hr.employee', blank=True, null=True, related_name='lead_member')

    #
    user = models.OneToOneField(User, verbose_name=u"账号绑定")
    # image: all image fields are base64 encoded and PIL-supported
    #image=models.ImageField(verbose_name=u"Photo")
    class Meta:
        db_table = 'hr.employee'
        verbose_name = '雇员'
        verbose_name_plural = "雇员"

    def __str__(self):
        return self.user.username

class department(models.Model):

    class Meta:
        db_table = 'hr.department'
        verbose_name = '部门'
        verbose_name_plural = "部门"

    name = models.CharField(verbose_name=u'Department Name',max_length=1024)
    parent = models.ForeignKey('hr.department', blank=True, null=True, related_name='dep_children')
    leader = models.ForeignKey('hr.employee', blank=True, null=True, related_name='emp_children')
    note=models.CharField(verbose_name=u'Note',max_length=1024)


    def __str__(self):
    #   dep_tree = _get_dep_tree(self)
        return self.name
    #
    # def _get_dep_tree(self):
    #     ret =''
    #     if (self.parent is not None):
    #         ret = _get_dep_tree(self.parent)
    #
    #     return ret + '/'+dep.name

