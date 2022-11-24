import django_filters
from django.db.models import Value, F
from django.db.models.functions import Concat, Lower, Trim, Coalesce, NullIf

from .models import *


class InstructorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method="filter_name", lookup_expr="icontains")
    username = django_filters.CharFilter(field_name="user__username", lookup_expr="icontains")

    def filter_name(self, queryset, name, value):
        string_full_name = Trim(Lower(Concat(F("user__first_name"), Value(' '), F("user__last_name"))))
        string_username = Trim(Lower(F("user__username")))
        if value is not None:
            queryset = queryset.annotate(
                name=Coalesce(NullIf(string_full_name, Value("")), string_username)).filter(name__icontains=value)
        return queryset

    class Meta:
        model = Instructor
        fields = ['name', 'username']
