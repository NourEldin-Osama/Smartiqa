from django.contrib import admin

# Register your models here.
from .models import User, Instructor, Course, Instructor_Courses

admin.site.register(User)
admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(Instructor_Courses)
