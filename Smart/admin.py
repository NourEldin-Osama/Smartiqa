from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User)
admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(Instructor_Courses)
admin.site.register(Recommendation_Course)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Attendance)
