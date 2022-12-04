from django import template
from django.urls import reverse
from random import sample
from Smart.models import *

register = template.Library()


@register.simple_tag
def active(current_link, active_link):
    if current_link == reverse(active_link):
        return "active"
    else:
        return ""


@register.simple_tag
def active_in(current_link, active_link):
    if active_link in current_link:
        return "active"
    else:
        return ""


@register.simple_tag
def lookup(dictionary, key):
    return dictionary.get(key)


@register.simple_tag
def course_editors(course_code, user_id):
    try:
        Instructor_Courses.objects.get(course=Course.objects.get(code=course_code),
                                       instructor=Instructor.objects.get(user=User.objects.get(id=user_id)))
    except:
        return False
    return True


@register.simple_tag
def shuffle(arg):
    return list(sample(arg, len(arg)))


@register.simple_tag
def to_list(*args):
    return list(args)


@register.simple_tag
def to_str(arg):
    return str(arg)

