from django import template

register = template.Library()

@register.filter()
def get_value(dictionary, arg):
    return dictionary.get(arg)