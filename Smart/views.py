import datetime

from django.conf import settings
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django_tables2 import RequestConfig
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from Smart.serializers import UserSerializer
from Smart.tables import *

default_theme = 'Light'
AVAILABLE_THEMES = ["Light", "Dark"]
AVAILABLE_MAJORS = ["Data Science - BSc", "Computer Science - BSc", "Computer Engineering - BSc",
                    "Electronics and Communications Engineering - BSc",
                    "Mechanical Engineering - BSc",
                    "Construction Engineering - BSc", "Actuarial Science - BSc",
                    "Architectural Engineering - BSc",
                    "Petroleum Engineering - BSc", "Physics - BS", "Mathematics - BSc",
                    "Biology - BSc", "Chemistry - BSc", ]


def anonymous_required(function=None, redirect_url=None):
    if not redirect_url:
        redirect_url = settings.LOGIN_REDIRECT_URL

    actual_decorator = user_passes_test(lambda u: u.is_anonymous, login_url=redirect_url)

    if function:
        return actual_decorator(function)
    return actual_decorator


# Create your views here.
def index(request):
    context = {"title": "Home"}
    return render(request, 'home.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return redirect('home')


@require_http_methods(["GET", "POST"])
@anonymous_required
def login(request):
    context = {'title': 'Login'}
    if request.method == "POST":
        u = auth.authenticate(username=request.POST['email'], password=request.POST['password'])
        if u is not None:
            auth.login(request, u)
            return redirect('home')
        else:
            try:
                username = User.objects.get(email=request.POST['email']).username
            except User.DoesNotExist:
                username = None
            u = auth.authenticate(username=username, password=request.POST['password'])
            if u is not None:
                auth.login(request, u)
                return redirect('home')
            context['error'] = "Username/Email or password is incorrect!"
    return render(request, 'User/login.html', context)


def create_new_user(request, Is_instructor=False):
    try:
        date = datetime.datetime.strptime(request.POST['birthdate'], "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        date = datetime.datetime.strptime(request.POST['birthdate'], "%d-%b-%Y").strftime("%Y-%m-%d")
    new_user = User(first_name=request.POST['first_name'], last_name=request.POST['last_name'],
                    gender=request.POST['gender'], username=request.POST['username'], email=request.POST['email'],
                    password=make_password(request.POST['password']), phone=request.POST['phone_number'],
                    birthdate=date, is_instructor=Is_instructor, major=request.POST['major'])
    if request.POST.get("picture", True):
        new_user.picture = request.FILES['picture']
    new_user.save()
    return new_user


@require_http_methods(["GET", "POST"])
@anonymous_required
def signup(request):
    context = {'title': 'Signup'}
    if request.method == "POST":
        if request.POST['password'] == request.POST['retyped_password']:
            if request.POST.get('terms', False) == 'agree':
                try:
                    User.objects.get(username=request.POST['username'])
                    context['error'] = 'Username is already taken!'
                except User.DoesNotExist:
                    try:
                        User.objects.get(username=request.POST['email'])
                        context['error'] = 'Email is already taken!'
                    except User.DoesNotExist:
                        new_user = create_new_user(request, Is_instructor=False)
                        return redirect('login')
            else:
                context['error'] = 'You must agree to the terms'
                return render(request, 'User/signup.html', context)
        else:
            context['error'] = 'Password does not match!'

    return render(request, 'User/signup.html', context)


@require_http_methods(["GET", "POST"])
@anonymous_required
def instructor_signup(request):
    context = {'title': 'Instructor Signup'}
    if request.method == "POST":
        if request.POST['password'] == request.POST['retyped_password']:
            if request.POST.get('terms', False) == 'agree':
                try:
                    User.objects.get(username=request.POST['username'])
                    context['error'] = 'Username is already taken!'
                except User.DoesNotExist:
                    try:
                        User.objects.get(username=request.POST['email'])
                        context['error'] = 'Email is already taken!'
                    except User.DoesNotExist:
                        new_user = create_new_user(request, Is_instructor=True)
                        new_instructor = Instructor(user=new_user, bio=request.POST['bio'],
                                                    job_title=request.POST['job_title'],
                                                    experience=request.POST['experience'])
                        new_instructor.save()
                        return redirect('login')
            else:
                context['error'] = 'You must agree to the terms'
                return render(request, 'Instructor/signup.html', context)
        else:
            context['error'] = 'Password does not match!'  # new_user.
    return render(request, 'Instructor/signup.html', context)


@login_required
def user_profile(request, user_name):
    context = {'title': 'Profile - Smartiqa'}
    if user_name == request.user.username:
        context['available_majors'] = AVAILABLE_MAJORS.copy()
        try:
            context['available_majors'].remove(request.user.major)
        except ValueError:
            pass
        if request.user.is_instructor:
            instructor = Instructor.objects.get(user=request.user.id)
            context["instructor"] = {'bio': instructor.bio, 'job_title': instructor.job_title,
                                     'experience': instructor.experience}
        return render(request, 'User/profile.html', context)
    else:
        context['error'] = "You Can't Show another user info"
        return render(request, 'home.html', context)


@login_required
def edit_user_profile(request, user_name):
    context = {'title': 'Edit User Profile - Smartiqa'}
    if request.method == "POST":
        if user_name == request.user.username:
            context['available_majors'] = AVAILABLE_MAJORS.copy()
            try:
                context['available_majors'].remove(request.user.major)
            except ValueError:
                pass
            user = User.objects.get(id=request.user.id)

            if request.POST.get("picture", True):
                user.picture = request.FILES['picture']

            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.gender = request.POST["gender"]
            user.major = request.POST["major"]

            # check if new username exist
            if request.POST["username"] != user.get_username():
                try:
                    User.objects.get(username=request.POST['username'])
                    context['error'] = 'Username is already taken!'
                    return render(request, 'User/profile.html', context)
                except User.DoesNotExist:
                    user.username = request.POST["username"]
                    user_name = user.username

            # check if new email exist
            if request.POST["email"] != user.email:
                try:
                    User.objects.get(email=request.POST['email'])
                    context['error'] = 'Email is already taken!'
                    return render(request, 'User/profile.html', context)
                except User.DoesNotExist:
                    user.email = request.POST["email"]

            if request.POST["password"] != "" and request.POST["password"] == request.POST["retyped_password"] and \
                    check_password(request.POST['old_password'], user.password):
                user.password = make_password(request.POST['password'])
            elif not check_password(request.POST['old_password'], user.password) and request.POST["password"] != "":
                context['error'] = 'Password Update Error!'
                return render(request, 'User/profile.html', context)
            user.phone_number = request.POST["phone_number"]

            if request.POST["birthdate"] != "":
                try:
                    date = datetime.datetime.strptime(request.POST['birthdate'], "%Y-%m-%d").strftime("%Y-%m-%d")
                except ValueError:
                    date = datetime.datetime.strptime(request.POST['birthdate'], "%d-%b-%Y").strftime("%Y-%m-%d")
                user.birthdate = date

            user.save()  # save changes after updates

            if user.is_instructor:
                instructor = Instructor.objects.get(user=user.id)
                instructor.bio = request.POST["bio"]
                instructor.job_title = request.POST["job_title"]
                instructor.experience = request.POST["experience"]
                instructor.save()  # save changes after updates

            # context["success"] = "your Info has been updated successfully"
            messages.success(request, 'Personal Information Updated.')

    # return render(request, 'User/profile.html', context)
    return redirect('profile', user_name)


@login_required
def settings(request):
    context = {"title": "settings - Smartiqa"}
    return render(request, 'User/settings.html', context)


@api_view(['POST'])
def set_theme(request, theme_value=''):
    response = Response({'message': 'Success'}, status=200)
    if not theme_value:
        response.set_cookie(key='Theme', value=default_theme, max_age=datetime.timedelta(days=365))
    elif theme_value in AVAILABLE_THEMES:
        response.set_cookie(key='Theme', value=theme_value, max_age=datetime.timedelta(days=365))
    return response


@api_view(['POST'])
def get_theme(request):
    if 'Theme' not in request.COOKIES:
        response = Response({'theme_value': default_theme}, status=200)
        response.set_cookie(key='Theme', value=default_theme, max_age=datetime.timedelta(days=365))
        return response
    else:
        return Response({'theme_value': request.COOKIES['Theme']}, status=200)


# Try
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


def instructor_profile(request, user_name):
    context = {"title": "instructor_profile - Smartiqa"}
    try:
        user = User.objects.get(username=user_name)
        if user.is_instructor:
            instructor = Instructor.objects.get(user=user)
            context["instructor"] = {'bio': instructor.bio,
                                     'job_title': instructor.job_title, 'experience': instructor.experience}
            context["instructor_data"] = {'name': user, 'picture': user.picture}
        else:
            messages.error(request, 'This instructor does not exist!')
            return redirect('view_instructors')
    except User.DoesNotExist:
        messages.error(request, 'This instructor does not exist!')
        return redirect('view_instructors')
    return render(request, 'Instructor/profile.html', context)


def view_instructors(request):
    context = {"title": "Instructors"}
    table = InstructorTable(Instructor.objects.all())
    RequestConfig(request).configure(table)
    context['table'] = table
    return render(request, 'Instructor/view.html', context)
