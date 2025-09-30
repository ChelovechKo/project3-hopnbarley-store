from django import template
register = template.Library()


@register.filter
def get_item(d, key):
    if key in d:
        return d.get(key)
