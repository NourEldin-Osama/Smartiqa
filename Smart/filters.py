import django_filters
from django.db.models import Value, F, Q
from django.db.models.functions import Concat, Lower, Trim, Coalesce, NullIf

from .models import *


class InstructorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method="filter_name", lookup_expr="icontains")
    username = django_filters.CharFilter(field_name="user__username", lookup_expr="icontains")
    name_username = django_filters.CharFilter(method="filter_name_username", lookup_expr="icontains")

    def filter_name(self, queryset, name, value):
        string_full_name = Lower(Trim(Concat(Trim(F("user__first_name")), Value(' '), Trim(F("user__last_name")))))
        string_username = Trim(Lower(F("user__username")))
        if value is not None:
            queryset = queryset.annotate(
                name=Coalesce(NullIf(string_full_name, Value("")), string_username)
            ).filter(name__icontains=value)
        return queryset

    def filter_name_username(self, queryset, name, value):
        string_full_name = Lower(Trim(Concat(Trim(F("user__first_name")), Value(' '), Trim(F("user__last_name")))))
        string_username = Trim(Lower(F("user__username")))
        if value is not None:
            queryset = queryset.annotate(
                name=Coalesce(NullIf(string_full_name, Value("")), string_username),
                username=F("user__username")
            ).filter(Q(name__icontains=value) | Q(username__icontains=value))
        return queryset

    class Meta:
        model = Instructor
        fields = ['name', 'username', 'name_username']
