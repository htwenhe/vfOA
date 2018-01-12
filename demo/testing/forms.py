from django import forms
from material import *

from . import models



class ContractForm(forms.ModelForm):

    class Meta:
        model = models.Contract
        fields = ['protocol_no',
        'task_no',
        'product_type',
        'product_num',
        'customer',
        'sample_from',
        'sample_to',
        'report_get',
        'testing_area',
        'report_num',
        'testing_class',
        'testing_time_class',
        'testing_time',
        'testing_standards',
        'testing_items',
        'testing_fee',
        'testing_fee_tax_no',
        'testing_fee_tax_class',
        ]
        widgets = {
            'testing_items':  forms.CheckboxSelectMultiple()
        }


    sample_from = forms.ChoiceField( label='来样方式' , choices=(('1', "送样"),('2', "邮寄"),))
    sample_to = forms.ChoiceField( label='样品处理' ,choices=(('1', "自取"),('2', "放弃"),('3', "邮寄"),('4', "留存"),))
    report_get = forms.ChoiceField( label='报告领取' ,choices=(('1', "自取"),('2', "邮寄"),))
    testing_area = forms.ChoiceField( label='测试地点' ,choices=(('1', "本中心"),('2', "现场"),))
    testing_class = forms.ChoiceField(label='检测类别' ,choices=(('1', "委托"),('2', "型检"),('3', "监督"),('4', "仲裁"),('4', "摸底"),('4', "检查"),))
    testing_time_class = forms.ChoiceField( label='检测时间' ,choices=(('1', "常规"),('2', "加急"),('2', "特急"),))
    testing_fee_tax_class = forms.ChoiceField( label='发票类别' ,choices=(('1', "增值税普通发票"),('2', "增值税专用发票"),))
    #testing_times = forms.MultipleChoiceField(label='测试项目A')


    # def __init__(self, *args, **kwargs):
    #     super(ContractCreateForm, self).__init__(*args, **kwargs)
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.id:
    #         self.fields['testing_items'].widget = forms.CheckboxSelectMultiple