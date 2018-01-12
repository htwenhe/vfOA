from django.views import generic
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from viewflow.decorators import flow_start_view, flow_view
from viewflow.flow.views import StartFlowMixin, FlowMixin
from viewflow.flow.views.utils import get_next_task_url
import django.utils.timezone as timezone
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from .forms import *
from .models import *


from viewflow.flow.views import (
    DetailProcessView as BaseDetailProcessView,
    CancelProcessView as BaseCancelProcessView
)
from viewflow.frontend.views import ProcessListView as BaseProcessListView
from viewflow.frontend.viewset import FlowViewSet


class ProcessListView(BaseProcessListView):

    list_display = [
        'process_id', 'process_summary',
        'created', 'resion','dep_approved_l','hr_approved_l','operate'
    ]

    filterset_fields = ['created',]
    list_filterset_fields= ('created',)


    def resion(self,process):
        return process.leave.resion

    def dep_approved_l(self,process):
        return self._get_appreve_html( process.dep_approved)

    def hr_approved_l(self,process):
        return self._get_appreve_html(process.hr_approved)

    def _get_appreve_html(self,approve):
        if approve == 1:
            return mark_safe('<span class="approve_ok_icon"/> ')
        elif approve == -1:
            return mark_safe('<span class="approve_ng_icon"/>')
        else:
            return ''

    def operate(self,process):
        return mark_safe(_('<a href="/leave/leave/action/delete/'+str(process.id)+'">删除</a>'))

    resion.short_description = _('原因')
    dep_approved_l.short_description = _('部门审核')
    hr_approved_l.short_description = _('人事审核')
    operate.short_description = _('操作')




    def get_queryset(self):
        querySet =  super(ProcessListView, self).get_queryset()
        # 只显示自己的申请
        return querySet.filter(leave__req_by__user=self.request.user)


def LeaveDel(request,process_pk):
    LeaveProcess.objects.filter(id=process_pk).delete()
    print('del==>'+str(process_pk))
    return HttpResponseRedirect("/leave/leave")

class DetailProcessView(BaseDetailProcessView):
    def get_queryset(self):
        return super(DetailProcessView, self).get_queryset()


class CancelProcessView(BaseCancelProcessView):
    def get_queryset(self):
        return super(CancelProcessView, self).get_queryset()


class LeaveFlowViewSet(FlowViewSet):
    # def get_process_queryset(self, request):
    #     pass

    process_list_view = [
        r'^$',
        ProcessListView.as_view(),
        'index'
    ]

    detail_process_view = [
        r'^(?P<process_pk>\d+)/$',
        DetailProcessView.as_view(),
        'detail'
    ]

    cancel_process_view = [
        r'^action/cancel/(?P<process_pk>\d+)/$',
        CancelProcessView.as_view(),
        'action_cancel'
]

class LeaveStartView(StartFlowMixin,generic.CreateView):

    form_class =LeaveForm

    template_name = 'leave/start.html'


    def get(self, request, *args, **kwargs):
        # 初始化数据
        self.initial = {'req_by':request.user.employee,
                    'depart_name':request.user.employee.department,
                    'position':'没有职位',
                    'req_date':timezone.now()}

        return super(LeaveStartView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        """If the form is valid, save the associated model and finish the task."""
        leave = form.save(commit=False)
        leave.req_by = self.request.user.employee
        leave.save()
        self.activation.process.leave=leave
        self.activation_done()
        return redirect(get_next_task_url(self.request, self.activation.process))


    layout = Layout(
        Fieldset('基本信息',Row('req_by','depart_name', 'position','req_date')),
        Fieldset('请假',Row('req_class', 'file_url'),
        Row('start_time','end_time'),
        'resion',)
    )

    # list_display = (
    #     'req_by', 'depart_name', 'req_date','resion',)

#该方法灵活度高，可自定义模板，展示内容。
@flow_view
def approve_check(request, **kwargs):
    request.activation.prepare(request.POST or None, user=request.user)

    if request.method == 'POST':

        dep_approved = request.POST.get('dep_approved', '')
        if dep_approved != '':
            request.activation.process.dep_approved = dep_approved
            request.activation.process.dep_approved_comment = request.POST.get('dep_approved_comment','')
            request.activation.process.dep_approved_time = timezone.now()

        hr_approved = request.POST.get('hr_approved', '')
        if hr_approved != '':
            request.activation.process.hr_approved = hr_approved
            request.activation.process.hr_approved_comment = request.POST.get('hr_approved_comment','')
            request.activation.process.hr_approved_time = timezone.now()

        request.activation.process.save()
        request.activation.done()
        return redirect(get_next_task_url(request, request.activation.process))

    else:
        leave = request.activation.process.leave
        if request.activation.process.dep_approved == True:
            form = LeaveHrCheckForm(instance=leave,initial={'dep_approved': request.activation.process.dep_approved,
                                                            'dep_approved_comment':request.activation.process.dep_approved_comment})

        else:
            form = LeaveDepCheckForm(instance=leave)

        return render(request, 'leave/check.html', {
            'form': form,
            'activation': request.activation
        })

def test(request):
    now = timezone.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)