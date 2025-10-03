from __future__ import annotations
from decimal import Decimal
from typing import Any, Dict, Iterator, TypedDict
from django.conf import settings
from django.http import HttpRequest

from products.models import Product


class StoredCartItem(TypedDict):
    """Хранение товара в сессии"""
    quantity: int
    price: str


class Cart:
    def __init__(self, request: HttpRequest) -> None:
        """Инициализация корзины"""
        self.session = request.session
        self.cart: Dict[str, StoredCartItem] = self.session.get(settings.CART_SESSION_ID, {})

    def get_quantity(self, product: Product) -> int:
        """Текущее кол-во товара в корзине"""
        pid = str(product.id)
        data = self.cart.get(pid)
        return int(data['quantity']) if data else 0

    def change_quantity(self, product: Product, to_add: int = 1) -> None:
        """Изменить количество товара в корзине на +-1 в зависимости от action"""
        product_id = str(product.id)
        self.cart.setdefault(product_id, {
            'quantity': 0,
            'price': str(product.price),
        })
        self.cart[product_id]['quantity'] += to_add

        if self.cart[product_id]['quantity'] <= 0:
            self.remove(product)
        else:
            self.save()

    def remove(self, product: Product) -> None:
        """Удаление товара из корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self) -> None:
        """Удаление корзины из сессии"""
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        """Перебор элементов в корзине и получение продуктов из базы данных"""
        product_ids = list(self.cart.keys())
        products = Product.objects.filter(id__in=product_ids)
        products_by_id = {str(p.id): p for p in products}

        for pid, data in self.cart.items():
            product = products_by_id.get(pid)
            if not product:
                continue
            price = Decimal(data['price'])
            quantity = int(data['quantity'])
            yield {
                'product': product,
                'price': price,
                'quantity': quantity,
                'total_price': price * quantity,
            }

    def __len__(self) -> int:
        """Подсчет количество всех товаров в корзине"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self) -> Decimal:
        """Подсчет стоимости товаров в корзине"""
        return sum((Decimal(item['price']) * item['quantity'] for item in self.cart.values()), Decimal("0"))

    def save(self) -> None:
        """Обновление сессии"""
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
