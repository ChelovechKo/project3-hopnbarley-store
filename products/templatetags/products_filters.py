from django import template
from django.http import HttpRequest

register = template.Library()


@register.filter(name='range')
def template_range(stop: int, start: int = 0) -> range:
    return range(start, stop)


@register.simple_tag()
def update_query_string(request: HttpRequest, value: str, key: str = 'page') -> str:
    params = request.GET.copy()
    params[key] = value
    return params.urlencode()
