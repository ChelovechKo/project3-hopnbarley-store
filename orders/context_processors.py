from typing import Any, Dict
from django.http import HttpRequest
from orders.cart import Cart


def cart(request: HttpRequest) -> Dict[str, Any]:
    return {'cart': Cart(request)}
