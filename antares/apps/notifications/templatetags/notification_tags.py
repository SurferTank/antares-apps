'''
Created on 28 sep. 2016

@author: leobelen
'''
from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def notification_badge_count(context):
    return ""
