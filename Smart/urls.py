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
    path('set_theme/', views.set_theme, name='set_theme'),
    path('set_theme/<str:theme_value>', views.set_theme, name='set_theme'),
    path('get_theme', views.get_theme, name='get_theme'),
    path('instructors', views.view_instructors, name='view_instructors'),
    path('instructor/<str:user_name>', views.instructor_profile, name='instructor'),
]
