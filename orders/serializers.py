from typing import Any, Dict
from decimal import Decimal
from django.db import transaction, models
from rest_framework import serializers

from orders.models import Order, OrderItem, OrderStatus
from products.models import Product
from orders.cart import Cart


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("id", "product", "quantity", "price")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "status", "total_price", "shipping_address", "create_at", "items")


class OrderCreateSerializer(serializers.Serializer):
    """Создание заказа на основании сессионной корзины."""
    city = serializers.CharField()
    address = serializers.CharField()
    payment_method = serializers.ChoiceField(choices=[("cod","cod"),("card","card")], default="cod")

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        request = self.context["request"]
        cart = Cart(request)
        if len(cart) == 0:
            raise serializers.ValidationError("Корзина пуста.")
        return attrs

    def create(self, validated_data: Dict[str, Any]) -> Order:
        request = self.context["request"]
        cart = Cart(request)
        items = list(cart)

        shipping_address = f"{validated_data['city']}, {validated_data['address']}"
        status = OrderStatus.PAID if validated_data.get("payment_method") != "cod" else OrderStatus.PENDING

        with transaction.atomic():
            # блокируем продукты, проверяем остатки
            product_ids = [i["product"].id for i in items]
            products_locked = Product.objects.select_for_update().filter(id__in=product_ids, is_active=True)
            products_by_id = {p.id: p for p in products_locked}

            for it in items:
                p = products_by_id.get(it["product"].id)
                if not p or it["quantity"] <= 0 or it["quantity"] > (p.stock or 0):
                    raise serializers.ValidationError(f"Недостаточно остатка для {it['product'].name}.")

            # списываем остатки
            for it in items:
                p = products_by_id[it["product"].id]
                p.stock = models.F("stock") - it["quantity"]
                p.save(update_fields=["stock"])

            # создаём ордер
            total = Decimal(cart.get_total_price())
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                status=status,
                total_price=total,
                shipping_address=shipping_address,
            )

            # итемы
            for it in cart:
                OrderItem.objects.create(
                    order=order,
                    product=it["product"],
                    price=it["price"],
                    quantity=it["quantity"],
                )

            cart.clear()

        return order

    def to_representation(self, instance: Order) -> Dict[str, Any]:
        from .serializers import OrderSerializer
        return OrderSerializer(instance, context=self.context).data