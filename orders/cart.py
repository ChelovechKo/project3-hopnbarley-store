from decimal import Decimal
from django.conf import settings
from products.models import Product


class Cart:
    # формат в сессии: { product_id: {'quantity': 1, 'price': '10.00'} }

    def __init__(self, request):
        """Инициализация корзины"""
        self.session = request.session
        self.cart = self.session.get(settings.CART_SESSION_ID, {})

    def change_quantity(self, product, to_add:int=1) -> None:
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

    def remove(self, product):
        """Удаление товара из корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """Удаление корзины из сессии"""
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def __iter__(self):
        """Перебор элементов в корзине и получение продуктов из базы данных"""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Подсчет количество всех товаров в корзине"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Подсчет стоимости товаров в корзине"""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def save(self):
        """Обновление сессии"""
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
