import django_tables2 as tables

from .models import *

ATTRIBUTES = {"class": "table table-striped dt-responsive table-hover table-bordered",
              "thead": {"class": "text-capitalize custom-table-head"},
              "tbody": {"class": "table-group-divider custom-table-body"},
              "th": {"class": ""}}


class UserTable(tables.Table):
    class Meta:
        model = User
        attrs = ATTRIBUTES
        orderable = False


class InstructorTable(tables.Table):
    user = tables.Column(accessor='user', verbose_name="full name")
    username = tables.URLColumn(accessor='user.username', verbose_name="username")
    major = tables.Column(accessor='user.major', verbose_name="major")

    class Meta:
        model = Instructor
        attrs = ATTRIBUTES
        orderable = False
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
