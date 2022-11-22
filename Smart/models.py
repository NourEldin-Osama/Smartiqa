from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    is_instructor = models.BooleanField('instructor status', default=False)
    email = models.EmailField(unique=True, default="", blank=True)
    birthdate = models.DateField(blank=True, null=True)
    MALE, FEMALE = 'M', 'F'
    TEMP_CHOICES = ((MALE, 'Male'), (FEMALE, 'Female'))
    gender = models.CharField(max_length=1, choices=TEMP_CHOICES, default=MALE)
    phone = models.CharField(max_length=15, default="+201000000000")
    picture = models.ImageField(default="", null=True)
    major = models.CharField(max_length=10, null=True, default="")

    def __str__(self):
        string_name = self.get_full_name()
        if string_name == "":
            string_name = self.username.strip()
        return string_name


class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(null=True, default="")
    job_title = models.CharField(max_length=255, null=True, default="")
    experience = models.TextField(null=True, default="")

    def __str__(self):
        string_name = self.user.get_full_name()
        if string_name == "":
            string_name = self.user.username.strip()
        return string_name

    class Meta:
        ordering = ["user"]


class Course(models.Model):
    name = models.CharField(max_length=50, default="")
    code = models.CharField(max_length=10, default="")
    hours = models.IntegerField()
    prerequisite = models.CharField(null=True, max_length=500)
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)
    location = models.TextField(null=True, default="")
    description = models.TextField(null=True, default="")
    beginner, intermediate, advanced, professional, expert = 'B', 'I', 'A', 'P', 'E'
    TEMP_CHOICES = (
        (beginner, 'Beginner'), (intermediate, 'Intermediate'), (advanced, 'Advanced'), (professional, 'Professional'),
        (expert, 'Expert'))
    level = models.CharField(max_length=1, choices=TEMP_CHOICES, default=beginner)
    link = models.CharField(max_length=2000, null=True, default="")

    def __str__(self):
        return self.name.strip()

    class Meta:
        ordering = ["-name"]


class Recommendation_Course(models.Model):
    title = models.CharField(max_length=50, default="")
    rating = models.DecimalField(decimal_places=2,max_digits=3)
    organization = models.CharField(max_length=200, null=True, default="")
    description = models.TextField(null=True, default="")
    beginner, intermediate, advanced, professional, expert = 'B', 'I', 'A', 'P', 'E'
    TEMP_CHOICES = (
        (beginner, 'Beginner'), (intermediate, 'Intermediate'), (advanced, 'Advanced'), (professional, 'Professional'),
        (expert, 'Expert'))
    difficulty = models.CharField(max_length=1, choices=TEMP_CHOICES, default=beginner)
    link = models.CharField(max_length=2000, null=True, default="")

    def __str__(self):
        return self.title.strip()

    class Meta:
        ordering = ["-title"]


class Instructor_Courses(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        string_name = self.instructor.user.get_full_name()
        if string_name == "":
            string_name = self.instructor.user.username.strip()
        return string_name + " (" + self.course.name.strip() + ")"
