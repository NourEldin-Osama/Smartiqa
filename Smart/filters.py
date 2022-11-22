import django_filters

from .models import *


class InstructorFilter(django_filters.FilterSet):
    class Meta:
        model = Instructor
        fields = "__all__"
