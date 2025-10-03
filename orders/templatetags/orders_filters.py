from django import template
from typing import Any, Mapping
register = template.Library()


@register.filter
def get_item(d: Mapping[str, Any], key: str) -> Any:
    if key in d:
        return d.get(key)
