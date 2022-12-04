from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('Logout', views.logout, name='Logout'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='student_signup'),
    path('instructor_signup', views.instructor_signup, name='instructor_signup'),
    path('settings', views.settings, name='settings'),
    path('user/<str:user_name>', views.user_profile, name='profile'),
    path('user/<str:user_name>/edit', views.edit_user_profile, name='edit_profile'),
    path('set_theme', views.set_theme, name='set_theme'),
    path('get_theme', views.get_theme, name='get_theme'),
    path('instructors', views.view_instructors, name='view_instructors'),
    path('instructor/<str:user_name>', views.instructor_profile, name='instructor'),
    path('courses', views.view_courses, name='view_courses'),
    path('create_course', views.create_course, name='create_course'),
    path('course/<str:code>', views.courses_page, name='course'),
    path('course/<str:code>/edit', views.edit_course, name='edit_course'),
    path('internet_courses', views.view_internet_courses, name='view_internet_courses'),
    path('tests', views.view_tests, name='tests'),
    path('test/<int:test_id>', views.test_page, name='test'),
    path('submit_exam/<int:test_id>', views.submit_exam, name='submit_exam'),
    path('attendance', views.attendance, name='attendance'),
    path('attendance/add', views.add_attendance, name='add_attendance'),
    path('attendance/facial_add', views.facial_add_attendance_page, name='facial_add_attendance'),
    path('attendance/facial_add/api', views.facial_add_attendance, name='facial_add_attendance_api'),
    path('facial_login/enable', views.enable_facial_login, name='enable_facial_login'),
    path('facial_login', views.facial_login, name='facial_login'),
]
