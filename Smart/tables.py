import django_tables2 as tables

from .models import *


class UserTable(tables.Table):
    class Meta:
        model = User
        attrs = {"class": "table table-striped dt-responsive table-hover"}
        orderable = True


class InstructorTable(tables.Table):
    class Meta:
        model = Instructor
        attrs = {"class": "table table-striped dt-responsive table-hover"}
        orderable = True


class CourseTable(tables.Table):
    class Meta:
        model = Course
        attrs = {"class": "table table-striped dt-responsive table-hover"}
        orderable = True


class Instructor_CoursesTable(tables.Table):
    class Meta:
        model = Instructor_Courses
        attrs = {"class": "table table-striped dt-responsive table-hover"}
        orderable = True
