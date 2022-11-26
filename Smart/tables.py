import django_tables2 as tables
from django.db.models import Value
from django.db.models.functions import Concat, Lower, Trim, Coalesce, NullIf
from django_tables2 import A

from .models import *

ATTRIBUTES = {"class": "table table-striped dt-responsive table-hover table-bordered",
              "thead": {"class": "text-capitalize custom-table-head"},
              "tbody": {"class": "table-group-divider custom-table-body"}, "th": {"class": ""}}


class UserTable(tables.Table):
    class Meta:
        model = User
        attrs = ATTRIBUTES
        orderable = False


class InstructorTable(tables.Table):
    user = tables.Column(accessor='user', verbose_name="full name")
    username = tables.Column(accessor='user__username', verbose_name="username",
                             linkify=("instructor", [A("user__username")]))  # (viewname, args)
    major = tables.Column(accessor='user.major', verbose_name="major")

    def order_user(self, queryset, is_descending):
        string_full_name = Lower(Trim(Concat(Trim(A("user__first_name")), Value(' '), Trim(A("user__last_name")))))
        string_username = Trim(Lower(A("user__username")))
        queryset = queryset.annotate(
            name=Coalesce(NullIf(string_full_name, Value("")), string_username)
        ).order_by(("-" if is_descending else "") + "name")
        return queryset, True

    class Meta:
        model = Instructor
        attrs = ATTRIBUTES
        orderable = True
        fields = ('user', 'job_title', 'username', 'major')
        sequence = ('user', 'job_title', 'username', 'major')


class CourseTable(tables.Table):
    class Meta:
        model = Course
        attrs = ATTRIBUTES
        orderable = False


class Instructor_CoursesTable(tables.Table):
    class Meta:
        model = Instructor_Courses
        attrs = ATTRIBUTES
        orderable = False
