from django import template

register = template.Library()

@register.filter
def div(value, arg):
    try:
        arg = float(arg)
        if arg == 0:
            return 0 
        return float(value) / arg
    except (ValueError, TypeError):
        return 0 
