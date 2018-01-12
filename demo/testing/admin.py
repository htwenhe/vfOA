from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
# Register your models here.
import django.utils.timezone as timezone
from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import *
from .forms import *
from django.core.urlresolvers import resolve

# Register your models here.


def complete_tasks(modeladmin, request, queryset):
    queryset.update(testing_status='1')
complete_tasks.short_description = '测试完成'

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):

    # def get_urls(self):
    #     pass

    # def get_fields(self, request, obj=None):
    #     pass
    #-----------------**********************
    #formfield_for_manytomany

    #------form---------------
    icon = "<i class='material-icons'>person</i>"
    form = ContractForm
    save_as = True
    layout = Layout(
        Fieldset('检测基本信息',
            Row('customer','protocol_no','task_no', 'product_type',),
            Row( 'product_num','sample_from', 'sample_to', 'report_get',),
            Row('testing_area','report_num',),
            Row('testing_class','testing_time_class', 'testing_time',)),
        Fieldset('检测依据',Row( 'testing_standards'), Row('testing_items')),
        Fieldset('检测费用',Row('testing_fee', 'testing_fee_tax_no','testing_fee_tax_class', ))
    )


    def _get_object_from_request(self,request):

        resolved = resolve(request.path_info)
        if resolved.args:
            return Contract.objects.get(pk=resolved.args[0])

        return None

    def formfield_for_manytomany(self, db_field, request, **kwargs):

        if  db_field.name == 'testing_items':
            contract = self._get_object_from_request(request)
            if contract is not None:
                kwargs["queryset"] = TestingItem.objects.filter(testing_type=contract.testing_type)
            else:
                testin_type_id = request.GET.get('testing-type','1')
                one_type = TestingType.objects.filter(id=testin_type_id)
                kwargs["queryset"] = TestingItem.objects.filter(testing_type=one_type)
            #kwargs.update({"columns":'5'})
        return super(ContractAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)



    def save_model(self, request, obj, form, change):
        if change:
            pass
        else:
            testin_type_id = request.GET.get('testing-type', '1')
            obj.create_datetime = timezone.now()
            obj.create_user = request.user
            obj.testing_type = TestingType.objects.filter(id=testin_type_id).first()

        super(ContractAdmin, self).save_model(request, obj, form, change)


    #-------list----------------
    list_display = ('protocol_no', 'customer_name', 'create_datetime', 'user_name','operate')
    list_filter = ('customer',)
    search_fields = ['protocol_no','customer__name','create_user__username']
    list_display_links = ['protocol_no',]
    filter_horizontal = ('testing_standards',)
    readonly_fields = ('operate',)
    ordering = ('-create_datetime',)

    actions = [complete_tasks,]

    def customer_name(self, contract):
        return contract.customer.name

    def user_name(self, contract):
        return contract.create_user.username


    def operate(self, contract):
        return mark_safe('<a href="/admin/testing/contract/' + str(contract.id) + '/change">修改</a>'
                        '&nbsp;|&nbsp;<a href="/admin/testing/contract/' + str(contract.id) + '/delete">删除</a>')

    operate.short_description = _('操作')



@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')

    # list_filter = ('req_by','depart_name','req_class')
    # search_fields = ('resion',)


@admin.register(TestingItem)
class TestingItemAdmin(admin.ModelAdmin):
    pass

@admin.register(TestingType)
class TestingTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(TestingStandard)
class TestingStandardAdmin(admin.ModelAdmin):
    pass

