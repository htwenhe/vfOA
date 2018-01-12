from django.conf.urls import url, include
from django.views import generic
from . import views

urlpatterns = [
    url('^$', generic.RedirectView.as_view(url='./employee/', permanent=False), name="index"),
    url('^employee/', include(views.EmployeeViewSet().urls)),
    url('^department/', include(views.DepartmentViewSet().urls)),
]