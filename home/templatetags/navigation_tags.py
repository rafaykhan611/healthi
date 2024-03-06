from django import template
from django.urls import resolve, reverse

register = template.Library()

@register.simple_tag
def is_active(request, url):
    if resolve(request.path_info).url_name == resolve(reverse(url)).url_name:
        return 'active'
    return ''
