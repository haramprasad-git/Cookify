from django.template import Library

register = Library()

@register.filter(name='veganity_icon')
def veganity_icon(veganity_value):
    if veganity_value == 1:
        return 'fa-leaf text-success'
    elif veganity_value == 2:
        return 'fa-drumstick text-danger'
    elif veganity_value == 3:
        return 'fa-egg text-warning'
    else:
        return ''