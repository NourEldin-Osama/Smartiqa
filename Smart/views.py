import datetime

import pandas as pd
import requests
from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import redirect, render
from django.utils.timezone import localdate
from django.views.decorators.http import require_http_methods
from django_tables2 import RequestConfig
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from Smart.filters import *
from Smart.serializers import UserSerializer
from Smart.tables import *

default_theme = 'Light'
AVAILABLE_THEMES = ["Light", "Dark"]
AVAILABLE_LEVELS = {"B": "Beginner", "I": "Intermediate", "A": "Advanced", }
AVAILABLE_MAJORS = ["Data Science - BSc", "Computer Science - BSc", "Computer Engineering - BSc",
                    "Electronics and Communications Engineering - BSc", "Mechanical Engineering - BSc",
                    "Construction Engineering - BSc", "Actuarial Science - BSc", "Architectural Engineering - BSc",
                    "Petroleum Engineering - BSc", "Physics - BS", "Mathematics - BSc", "Biology - BSc",
                    "Chemistry - BSc", ]


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
            context['error'] = 'Password does not match!'

    return render(request, 'User/signup.html', context)


@require_http_methods(["GET", "POST"])
@anonymous_required
def instructor_signup(request):
    context = {'title': 'Instructor Signup'}
    if request.method == "POST":
        if request.POST['password'] == request.POST['retyped_password']:
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

            if request.POST["password"] != "" and request.POST["password"] == request.POST[
                "retyped_password"] and check_password(request.POST['old_password'], user.password):
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
def set_theme(request):
    theme_value = request.POST.get("theme_value", default_theme)
    response = Response({'message': 'Success'}, status=200)
    if not theme_value:
        response.set_cookie(key='Theme', value=default_theme, max_age=datetime.timedelta(days=365))
    elif theme_value in AVAILABLE_THEMES:
        response.set_cookie(key='Theme', value=theme_value, max_age=datetime.timedelta(days=365))
    return response


@api_view(['POST'])
def get_theme(request):
    if 'Theme' not in request.COOKIES or request.COOKIES['Theme'] not in AVAILABLE_THEMES:
        response = Response({'theme_value': default_theme, 'first_time': 'Y'}, status=200)
        response.set_cookie(key='Theme', value=default_theme, max_age=datetime.timedelta(days=365))
        return response
    else:
        return Response({'theme_value': request.COOKIES['Theme'], 'first_time': 'N'}, status=200)


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
            context["instructor"] = {'bio': instructor.bio, 'job_title': instructor.job_title,
                                     'experience': instructor.experience}
            context["instructor_data"] = {'name': user, 'picture': user.picture, 'username': user_name}
        else:
            messages.error(request, 'This instructor does not exist!')
            return redirect('view_instructors')
    except User.DoesNotExist:
        messages.error(request, 'This instructor does not exist!')
        return redirect('view_instructors')
    return render(request, 'Instructor/profile.html', context)


def view_instructors(request):
    context = {"title": "Instructors"}
    data = Instructor.objects.select_related('user').all()
    filtered_data = InstructorFilter(request.GET, queryset=data)
    table = InstructorTable(filtered_data.qs, order_by="user")
    RequestConfig(request, paginate={"per_page": 8}).configure(table)
    context['table'] = table
    context['filter'] = filtered_data
    return render(request, 'Instructor/view.html', context)


def view_courses(request):
    context = {"title": "Courses"}
    data = Instructor_Courses.objects.select_related('course', 'instructor').all()
    filtered_data = Instructor_CoursesFilter(request.GET, queryset=data)
    table = Instructor_CoursesTable(filtered_data.qs, order_by="name")
    RequestConfig(request, paginate={"per_page": 8}).configure(table)
    context['table'] = table
    context['filter'] = filtered_data
    return render(request, 'Course/view.html', context)


def courses_page(request, code):
    context = {"title": "Course Page - Smartiqa"}
    try:
        course = Course.objects.get(code=code)
    except Course.DoesNotExist:
        messages.error(request, 'This course does not exist!')
        return redirect('view_courses')
    context['course'] = {"name": course.name, "code": course.code, "hours": course.hours,
                         "prerequisite": course.prerequisite, "start": course.start, "end": course.end,
                         "location": course.location, "description": course.description, "level": course.level,
                         "level_text": AVAILABLE_LEVELS[course.level], "link": course.link}
    context['available_levels'] = AVAILABLE_LEVELS.copy()
    try:
        context['available_levels'].pop(course.level)
    except ValueError:
        pass
    return render(request, 'Course/page.html', context)


def edit_course(request, code):
    context = {"title": "Edit Course - Smartiqa"}
    if request.method == "POST":
        if request.user.is_instructor:
            try:
                course = Course.objects.get(code=code)
                old_course_code = course.code
                try:
                    instructor = Instructor.objects.get(user=request.user)
                    ic = Instructor_Courses.objects.get(course=course, instructor=instructor)
                except:
                    messages.error(request, "You can't edit this Course!")
                    return redirect('view_courses')
                try:
                    course = Course.objects.get(code=request.POST["code"])
                    if not course.code == request.POST["code"]:
                        messages.error(request, F"you can not use '{request.POST['code']}' as course code!")
                        return redirect('course', code)
                except Course.DoesNotExist:
                    course.code = request.POST["code"]
                    course.save()
                    old_course = Course.objects.get(code=old_course_code)
                    Instructor_Courses.objects.filter(course=old_course).update(course=course)
                    old_course.delete()
                course = Course.objects.get(code=request.POST["code"])
                course.name = request.POST["name"]
                course.hours = request.POST["hours"]
                course.prerequisite = request.POST["prerequisite"]
                course.start = request.POST["start"]
                course.end = request.POST["end"]
                course.location = request.POST["location"]
                course.description = request.POST["description"]
                course.level = request.POST["level"]
                course.link = request.POST["link"]
                course.save()
            except Course.DoesNotExist:
                messages.error(request, "This course does not exist!")
                return redirect('view_courses')
    course = Course.objects.get(code=request.POST["code"])
    context['course'] = {"name": course.name, "code": course.code, "hours": course.hours,
                         "prerequisite": course.prerequisite, "start": course.start, "end": course.end,
                         "location": course.location, "description": course.description, "level": course.level,
                         "level_text": AVAILABLE_LEVELS[course.level], "link": course.link}
    context['available_levels'] = AVAILABLE_LEVELS.copy()
    try:
        context['available_levels'].pop(course.level)
    except ValueError:
        pass
    return render(request, 'Course/page.html', context)


def view_internet_courses(request):
    context = {"title": "Internet Courses"}
    data = Recommendation_Course.objects.all()
    filtered_data = Recommendation_CourseFilter(request.GET, queryset=data)
    table = Recommendation_CourseTable(filtered_data.qs, order_by="name")
    RequestConfig(request, paginate={"per_page": 8}).configure(table)
    context['table'] = table
    context['filter'] = filtered_data
    return render(request, 'OnlineCourse/view.html', context)


def view_tests(request):
    context = {"title": "Tests"}
    data = Test.objects.all()
    filtered_data = TestFilter(request.GET, queryset=data)
    table = TestTable(filtered_data.qs, order_by="name")
    RequestConfig(request, paginate={"per_page": 8}).configure(table)
    context['table'] = table
    context['filter'] = filtered_data
    return render(request, 'Test/test.html', context)


@login_required
def create_course(request):
    if request.user.is_instructor:
        context = {"title": "Create Course - Smartiqa", 'available_levels': AVAILABLE_LEVELS.copy()}
        if request.method == "POST":
            try:
                context['available_levels'].pop(request.POST['level'])
            except ValueError:
                pass
            try:
                course = Course.objects.get(code=request.POST["code"])
                messages.error(request, F"this course code '{request.POST['code']}' is taken!")
                context['course'] = {"name": request.POST["name"], "code": request.POST["code"],
                                     "hours": request.POST["hours"], "prerequisite": request.POST["prerequisite"],
                                     "start": request.POST["start"], "end": request.POST["end"],
                                     "location": request.POST["location"], "description": request.POST["description"],
                                     "level": request.POST["level"],
                                     "level_text": AVAILABLE_LEVELS[request.POST["level"]],
                                     "link": request.POST["link"], }
                return render(request, 'Course/create.html', context)
            except Course.DoesNotExist:
                course = Course(name=request.POST["name"], code=request.POST["code"], hours=request.POST["hours"],
                                prerequisite=request.POST["prerequisite"], start=request.POST["start"],
                                end=request.POST["end"], location=request.POST["location"],
                                description=request.POST["description"], level=request.POST["level"],
                                link=request.POST["link"], )
                course.save()
                Instructor_Courses(course=course, instructor=Instructor.objects.get(user=request.user)).save()
                messages.success(request, F"{course} Course Created successfully!")
                return redirect("course", course.code)
        return render(request, 'Course/create.html', context)
    else:
        messages.error(request, "you can not create course!")
        return redirect('view_courses')


@login_required()
def test_page(request, test_id):
    try:
        test = Test.objects.get(id=test_id)
    except Test.DoesNotExist:
        messages.error(request, 'This test does not exist!')
        return redirect('tests')
    context = {"title": F"{test.name} Test - Smartiqa", "test": test}
    questions = Question.objects.filter(test=test).order_by('id')
    context['questions'] = questions
    return render(request, 'Test/page.html', context)


@login_required()
def submit_exam(request, test_id):
    try:
        test = Test.objects.get(id=test_id)
    except Test.DoesNotExist:
        messages.error(request, 'This test does not exist!')
        return redirect('tests')
    context = {"title": F"{test.name} Test - Smartiqa", "test": test}
    questions = Question.objects.filter(test=test).order_by('id')
    counter = 0
    if questions:
        for q in questions:
            q_answer = request.POST.get(str(q.id), "")
            if q_answer == q.right_ans:
                counter += 1
    context['num_correct_answer'] = counter
    num_questions = questions.count()
    percent = round(counter / num_questions, 2) * 100
    context['correct_answer_percent'] = percent
    context['questions'] = questions
    context['num_questions'] = num_questions
    user_answers = request.POST.dict()
    user_answers.pop('csrfmiddlewaretoken')
    user_answers.pop('cheated')
    context['user_answers'] = user_answers
    context['cheated'] = request.POST.get('cheated', True) == "True"
    if percent in range(25):
        level, color = "beginner", "red"
    elif percent in range(25, 50):
        level, color = "intermediate", "orange"
    elif percent in range(50, 75):
        level, color = "advanced", "yellow"
    else:
        level, color = "professional", "green"
    context['level'] = level
    context['color'] = color
    return render(request, 'Test/page.html', context)


@login_required()
def attendance(request):
    context = {"title": "Attendance"}
    if request.user.is_instructor:
        instructor = Instructor.objects.get(user=request.user)
        data = Attendance.objects.all().filter(instructor=instructor)
        filtered_data = AttendanceFilter(request.GET, queryset=data)
        table = AttendanceTable(filtered_data.qs, order_by="name")
        table.exclude = ("instructor",)
    elif request.user.is_superuser:
        data = Attendance.objects.all()
        filtered_data = AttendanceFilter(request.GET, queryset=data)
        table = AttendanceTable(filtered_data.qs, order_by="name")
    else:
        messages.error(request, "you can not View this page, Instructors Only!")
        return redirect("home")
    context["All"] = filtered_data.qs.count()
    context["Attendees"] = filtered_data.qs.filter(state=True).count()
    context["Absents"] = context["All"] - context["Attendees"]
    RequestConfig(request, paginate={"per_page": 8}).configure(table)
    context['table'] = table
    context['filter'] = filtered_data
    return render(request, 'Attendance/attendance.html', context)


def duplicate_data(name, date, state, instructor, course):
    try:
        Attendance.objects.get(name=name, date=date, state=state, instructor=instructor, course=course)
        return True
    except Attendance.DoesNotExist:
        return False


@login_required()
def add_attendance(request):
    context = {"title": "Add Attendance"}
    if request.user.is_instructor or request.user.is_superuser:
        if request.method == "POST":
            if request.POST.get("excel_file", True):
                file_name = request.FILES['excel_file']
                file_ext = file_name.name.split(".")[-1].lower()
                found_missing_col = False
                if file_ext == "csv":
                    data = pd.read_csv(request.FILES['excel_file'])
                    if "Date" in data.columns:
                        data["Date"] = pd.to_datetime(data["Date"])
                    else:
                        found_missing_col = True
                elif file_ext in ["xlsx", "xls"]:
                    data = pd.read_excel(request.FILES['excel_file'])
                else:
                    messages.error(request, "⚠️Not Supported File, the file Must be xlsx or xls or csv !")
                    return redirect("add_attendance")
                MUST_COL = ['Name', 'Course', 'Date', 'State']
                if not request.user.is_instructor:
                    MUST_COL.append('Instructor')
                for col in MUST_COL:
                    if col not in data.columns:
                        if col != "Date" or file_ext != "csv":
                            messages.error(request,
                                           F"⚠️Required Column '{col}' is missing, the file Must contain {col} column!")
                            found_missing_col = True
                if found_missing_col:
                    return redirect("add_attendance")
                duplicate = 0
                for _, record in data.iterrows():
                    A_Name, A_Date, A_State, A_Course = record["Name"], record["Date"], record["State"], record[
                        "Course"]
                    A_Course = Course.objects.get(code=str(A_Course))
                    if not request.user.is_instructor:
                        A_Instructor = Instructor.objects.get(user_id=str(record["Instructor"]))
                    else:
                        A_Instructor = Instructor.objects.get(user=request.user)
                    if duplicate_data(name=A_Name, date=A_Date, state=A_State, instructor=A_Instructor,
                                      course=A_Course):
                        duplicate += 1
                    else:
                        Attendance(name=A_Name, date=A_Date, state=A_State, instructor=A_Instructor,
                                   course=A_Course).save()
                if duplicate > 0:
                    messages.success(request, F"Upload Completed, {len(data)} row found, {duplicate} duplicate found!")
                    messages.success(request, F"{len(data) - duplicate} New rows.")
                else:
                    messages.success(request, F"Upload Completed Successfully, {len(data)} row found.")
                    messages.success(request, F"{len(data)} New rows.")
    else:
        messages.error(request, "you can not View this page, Instructors Only!")
        return redirect("home")
    return render(request, 'Attendance/add.html', context)


@login_required
def enable_facial_login(request):
    User.objects.filter(id=request.user.id).update(facial_login=True)
    return redirect("settings")


@api_view(['POST'])
def facial_login(request):
    if request.method == 'POST':
        frame = request.POST.get('image')
        payload = {'image': frame}
        r = requests.post("https://facialauthentication.pythonanywhere.com/recognize_user", data=payload)
        if r.status_code == 200 and r.json()['username'] != "":
            u = User.objects.get(username=r.json()['username'])
            auth.login(request, u, backend='django.contrib.auth.backends.ModelBackend')
            return Response({'result': "Done"}, status=200)
    return Response({'result': "Fail"}, status=200)


@login_required()
@api_view(['POST'])
def facial_add_attendance(request):
    if request.method == 'POST':
        frame = request.POST.get('image')
        course = request.POST.get('course')
        payload = {'image': frame}
        try:
            course = Course.objects.get(code=str(course))
        except Course.DoesNotExist:
            return Response({'result': "Fail, Course does not Exist"}, status=200)
        r = requests.post("https://facialauthentication.pythonanywhere.com/recognize_user", data=payload)
        if r.status_code == 200 and r.json()['username'] != "":
            u = User.objects.get(username=r.json()['username'])
            string_name = u.get_full_name()
            if string_name == "":
                string_name = u.username.strip()
            try:
                instructor = Instructor.objects.get(user=request.user)
            except Instructor.DoesNotExist:
                return Response({'result': "Fail, Instructor only"}, status=200)
            if not duplicate_data(name=string_name, date=localdate(), state=True, instructor=instructor, course=course):
                Attendance(name=string_name, date=localdate(), state=True, instructor=instructor, course=course).save()
                return Response({'result': F"Success, {string_name} now is registered as attendant"}, status=200)
            else:
                return Response({'result': F"Duplicate, {string_name} already registered as attendant"}, status=200)
    return Response({'result': "Fail, may be this student is not registered"}, status=200)


@login_required()
def facial_add_attendance_page(request):
    context = {"title": "Add Facial Login"}
    try:
        instructor = Instructor.objects.get(user=request.user)
    except Instructor.DoesNotExist:
        messages.error(request, 'you are not Instructor, Instructors only!')
        return redirect('attendance')
    courses = Instructor_Courses.objects.all().filter(instructor=instructor).select_related('course').values(
        'course_id', 'course__name')
    context["courses"] = courses
    return render(request, 'Attendance/facial_add.html', context)
