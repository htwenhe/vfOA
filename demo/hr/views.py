from material.frontend.views import ModelViewSet
from . import models

class EmployeeViewSet(ModelViewSet):

    model = models.employee

class DepartmentViewSet(ModelViewSet):

    model = models.department