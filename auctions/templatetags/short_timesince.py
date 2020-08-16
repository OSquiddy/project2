from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def upto(value):
    return value.split(',')[0]
upto.is_safe = True