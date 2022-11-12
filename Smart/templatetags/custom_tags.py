from django import template
from ..models import User
from django.db.models import Count
from django.urls import reverse

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
