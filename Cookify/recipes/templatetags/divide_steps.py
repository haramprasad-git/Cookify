from django import template

register = template.Library()

@register.filter(name='divide_steps')
def divide_steps(discription):
    for index, step in enumerate(discription.split('\n')):
        yield (index, step)