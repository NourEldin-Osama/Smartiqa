import django_tables2 as tables
from django.db.models import Value
from django.db.models.functions import Concat, Lower, Trim, Coalesce, NullIf
from django_tables2 import A

from .models import *

ATTRIBUTES = {"class": "table table-striped dt-responsive table-hover table-bordered",
              "thead": {"class": "text-capitalize custom-table-head", "style": "white-space: nowrap;"},
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
        queryset = queryset.annotate(name=Coalesce(NullIf(string_full_name, Value("")), string_username)).order_by(
            ("-" if is_descending else "") + "name")
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
    name = tables.Column(accessor='course__name', verbose_name="Course Name")
    instructor = tables.Column(accessor='instructor__user__username', verbose_name="Instructor Username",
                               linkify=("instructor", [A("instructor__user__username")]))  # (viewname, args)
    code = tables.Column(accessor='course__code', verbose_name="Course Code",
                         linkify=("course", [A("course__code")]))  # (viewname, args)
    level = tables.Column(accessor='course__level', verbose_name="Course Level")

    class Meta:
        model = Instructor_Courses
        attrs = ATTRIBUTES
        orderable = True
        fields = ('name', 'instructor', 'code', 'level')
        sequence = ('name', 'instructor', 'code', 'level')


class Recommendation_CourseTable(tables.Table):
    url = tables.URLColumn(accessor='url', verbose_name="Url", attrs={"a": {"target": "_blank"}})

    class Meta:
        model = Recommendation_Course
        attrs = ATTRIBUTES
        orderable = True
        fields = (
            "name", "organization", "hours", "user_rating", "total_ratings", "total_enrollments", "difficulty", "url",)
        sequence = (
            "name", "organization", "hours", "user_rating", "total_ratings", "total_enrollments", "difficulty", "url",)


class TestTable(tables.Table):
    code = '<a class="btn btn-primary" href="{% url "test" value %}" role="button">Start Exam</a>'
    button = tables.TemplateColumn(template_code=code, accessor="id", verbose_name="", orderable=False,
                                   attrs={"a": {"target": "_blank"}, "td": {"class": "text-center"}})

    class Meta:
        model = Test
        attrs = ATTRIBUTES
        orderable = True
        fields = ("name", "field", "button",)
        sequence = ("name", "field", "button",)


class AttendanceTable(tables.Table):
    instructor = tables.Column(accessor='instructor__user__username', verbose_name="Instructor",
                               linkify=("instructor", [A("instructor__user__username")]),
                               attrs={"a": {"target": "_blank"}, "td": {"class": "text-center"}})

    class Meta:
        model = Attendance
        attrs = ATTRIBUTES
        orderable = True
        fields = ("name", "course", "date", "state", "instructor")
        sequence = ("name", "course", "date", "state", "instructor")
