from django import template

register = template.Library()

@register.filter(name='all_below')
def all_below(stop):
    return range(stop)