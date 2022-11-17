import django_tables2 as tables

from .models import *

ATTRIBUTES = {"class": "table table-striped dt-responsive table-hover table-bordered",
              "thead": {"class": "text-capitalize"},
              "tbody": {"class": "table-group-divider"},
              "th": {"class": ""}}


class UserTable(tables.Table):
    class Meta:
        model = User
        attrs = ATTRIBUTES
        orderable = False


class InstructorTable(tables.Table):
    class Meta:
        model = Instructor
        attrs = ATTRIBUTES
        orderable = False


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
