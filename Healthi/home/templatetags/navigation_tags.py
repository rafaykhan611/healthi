from django import template
from django.urls import resolve, reverse
import math

register = template.Library()

@register.simple_tag
def is_active(request, url):
    if resolve(request.path_info).url_name == resolve(reverse(url)).url_name:
        return 'active'
    return ''

@register.filter(name='floor_range')
def floor_range(value):
    return range(1, math.floor(value) + 1)

@register.filter(name='floor')
def floor(value):
    return math.floor(value)

@register.filter(name='has_decimal')
def has_decimal(value, threshold=0.01):
    return abs(value - int(value)) > threshold