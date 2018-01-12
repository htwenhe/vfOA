from .views import *
from .flows import LeaveFlow
from django.conf.urls import url, include
from django.views import generic


urlpatterns = [
    url('^$', generic.RedirectView.as_view(url='./leave/'), name="index"),
    url('^leave/', include(LeaveFlowViewSet(LeaveFlow).urls),name="leave"),
    url('^leave/action/delete/(?P<process_pk>\d+)/$',LeaveDel, name="delete"),
]
