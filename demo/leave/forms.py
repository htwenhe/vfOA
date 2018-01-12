from django import forms
from material import *

from . import models


class LeaveForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LeaveForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        #不起作用
        if instance and instance.id:
            self.fields['req_by'].widget.attrs['disabled'] = True
            self.fields['position'].widget.attrs['readonly'] = True
            self.fields['depart_name'].widget.attrs['disabled'] = True
            self.fields['req_date'].widget.attrs['disabled'] = True


    class Meta:
        model = models.Leave
        fields = ['req_by','depart_name','position','req_date','req_class','file_url','start_time','end_time','resion',]
        widgets = {
            'password': forms.PasswordInput()
        }

class LeaveDepCheckForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LeaveDepCheckForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['position'].widget.attrs['readonly'] = True
            self.fields['resion'].widget.attrs['readonly'] = True
            self.fields['file_url'].widget.attrs['readonly'] = True
            self.fields['req_by'].widget.attrs['disabled'] = True
            self.fields['depart_name'].widget.attrs['disabled'] = True
            self.fields['req_date'].widget.attrs['disabled'] = True
            self.fields['start_time'].widget.attrs['disabled'] = True
            self.fields['end_time'].widget.attrs['disabled'] = True
            self.fields['req_class'].widget.attrs['disabled'] = True


    layout = Layout(
        Row(Span2('req_by'), 'depart_name', Span2('position'),'req_date'),
        Row('req_class', 'file_url'),
        Row('start_time','end_time'),
        'resion',
        'dep_approved',
        'dep_approved_comment',
    )
    dep_approved =forms.ChoiceField(label='部门审核',choices=((1, "同意"),
            (-1, "不同意"),))
    dep_approved_comment = forms.CharField(label='审核意见',widget=forms.Textarea)

    class Meta:
        model = models.Leave
        fields = ['req_by','depart_name', 'position', 'req_date', 'req_class', 'file_url', 'start_time', 'end_time', 'resion', 'dep_approved','dep_approved_comment']



class LeaveHrCheckForm(LeaveDepCheckForm):

    class Meta:
        model = models.Leave
        fields = ['req_by','depart_name', 'position', 'req_date', 'req_class', 'file_url', 'start_time', 'end_time', 'resion', 'dep_approved','dep_approved_comment','hr_approved','hr_approved_comment']


    layout = Layout(
        Row(Span2('req_by'), 'depart_name', Span2('position'),'req_date'),
        Row('req_class', 'file_url'),
        Row('start_time','end_time'),
        'resion',
        'dep_approved',
        'dep_approved_comment',
        'hr_approved',
        'hr_approved_comment',
    )

    hr_approved =forms.ChoiceField(label='人事审核',choices=((1, "同意"),
            (-1, "不同意"),))
    hr_approved_comment = forms.CharField(label='审核意见',widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(LeaveHrCheckForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['dep_approved'].widget.attrs['disabled'] = True
            self.fields['dep_approved_comment'].widget.attrs['readonly'] = True