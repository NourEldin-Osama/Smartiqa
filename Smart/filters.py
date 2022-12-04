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
            queryset = queryset.annotate(name=Coalesce(NullIf(string_full_name, Value("")), string_username)).filter(
                name__icontains=value)
        return queryset

    def filter_name_username(self, queryset, name, value):
        string_full_name = Lower(Trim(Concat(Trim(F("user__first_name")), Value(' '), Trim(F("user__last_name")))))
        string_username = Trim(Lower(F("user__username")))
        if value is not None:
            queryset = queryset.annotate(name=Coalesce(NullIf(string_full_name, Value("")), string_username),
                                         username=F("user__username")).filter(
                Q(name__icontains=value) | Q(username__icontains=value))
        return queryset

    class Meta:
        model = Instructor
        fields = ['name', 'username', 'name_username']


class Instructor_CoursesFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method="course__name", lookup_expr="icontains")
    code = django_filters.CharFilter(method="course__code", lookup_expr="icontains")
    name_code = django_filters.CharFilter(method="filter_name_code", lookup_expr="icontains")
    instructor = django_filters.CharFilter(method="filter_instructor_username", lookup_expr="icontains")

    def filter_name_code(self, queryset, name, value):
        if value is not None:
            queryset = queryset.annotate(name=F("course__name"), code=F("course__code")).filter(
                Q(name__icontains=value) | Q(code__icontains=value))
        return queryset

    def filter_instructor_username(self, queryset, name, value):
        if value is not None:
            queryset = queryset.annotate(username=F("instructor__user__username")).filter(Q(username__icontains=value))
        return queryset

    class Meta:
        model = Instructor_Courses
        fields = ['name', 'code', 'instructor', 'name_code']


class Recommendation_CourseFilter(django_filters.FilterSet):
    name_organization = django_filters.CharFilter(method="filter_name_organization", lookup_expr="icontains")

    def filter_name_organization(self, queryset, name, value):
        if value is not None:
            queryset = queryset.filter(Q(name__icontains=value) | Q(organization__icontains=value))
        return queryset

    class Meta:
        model = Recommendation_Course
        fields = ["name", "organization", "name_organization", "user_rating", "difficulty"]


class TestFilter(django_filters.FilterSet):
    name_field = django_filters.CharFilter(method="filter_name_field", lookup_expr="icontains")

    def filter_name_field(self, queryset, name, value):
        if value is not None:
            queryset = queryset.filter(Q(name__icontains=value) | Q(field__icontains=value))
        return queryset

    class Meta:
        model = Test
        fields = ["name", "field", "name_field"]


class AttendanceFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    course = django_filters.CharFilter(field_name="course__name", lookup_expr="icontains")
    name_course = django_filters.CharFilter(method="filter_name_course", lookup_expr="icontains")

    def filter_name_course(self, queryset, name, value):
        if value is not None:
            queryset = queryset.filter(Q(name__icontains=value) | Q(course__name__icontains=value))
        return queryset

    class Meta:
        model = Attendance
        fields = ["name", "course", "name_course"]
