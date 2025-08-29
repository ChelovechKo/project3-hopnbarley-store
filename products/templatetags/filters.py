from django import template

register = template.Library()


@register.filter(name='range')
def template_range(number):
    return range(number)
