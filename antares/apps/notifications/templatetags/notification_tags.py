'''
Created on 28 sep. 2016

@author: leobelen
'''
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def notification_badge_count(context):
    return ""
