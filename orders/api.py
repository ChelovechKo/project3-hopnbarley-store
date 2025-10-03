from typing import Any
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from config.permissions import IsAuthenticatedOrSessionForCart, IsOwner
from rest_framework import serializers, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models.query import QuerySet

from orders.serializers import OrderSerializer, OrderCreateSerializer
from orders.cart import Cart
from products.models import Product
from orders.models import Order


@extend_schema_view(
    list=extend_schema(tags=["Orders"], summary="Список заказов текущего пользователя"),
    retrieve=extend_schema(tags=["Orders"], summary="Детали заказа"),
    create=extend_schema(tags=["Orders"], summary="Создать заказ из корзины"),
    partial_update=extend_schema(tags=["Orders"]),
    destroy=extend_schema(tags=["Orders"]),
)
class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Order.objects.all()

    def get_queryset(self) -> QuerySet[Order]:
        request: Request = self.request
        assert request.user.is_authenticated
        return (
            Order.objects
            .filter(user_id=request.user.id)
            .prefetch_related("items", "items__product")
        )

    def get_serializer_class(self) -> type[serializers.BaseSerializer]:
        return OrderCreateSerializer if self.action == "create" else OrderSerializer

    def perform_create(self, serializer: serializers.BaseSerializer) -> None:
        serializer.save(user=self.request.user)


class CartView(APIView):
    permission_classes = [IsAuthenticatedOrSessionForCart]

    def _serialize_cart(self, request: Request) -> dict[str, Any]:
        cart = Cart(request)
        items = [{
            "product": it["product"].id,
            "name": it["product"].name,
            "price": str(it["price"]),
            "quantity": it["quantity"],
            "total_price": str(it["total_price"]),
        } for it in cart]
        return {"items": items, "total": str(cart.get_total_price())}

    def get(self, request: Request) -> Response:
        return Response(self._serialize_cart(request))

    def post(self, request: Request, pk: int) -> Response:
        """Добавить/изменить позицию: {product_id, action: increase|decrease|remove}"""
        raw_id = request.data.get("product_id")
        if raw_id is None:
            return Response({"detail": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        action = str(request.data.get("action", "increase"))

        try:
            product_id = int(raw_id)
        except (TypeError, ValueError):
            return Response({"detail": "product_id must be int"}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, id=product_id, is_active=True)

        cart = Cart(request)
        if action == "increase":
            cart.change_quantity(product, 1)
        elif action == "decrease":
            cart.change_quantity(product, -1)
        elif action == "remove":
            cart.remove(product)
        else:
            return Response({"detail": "unknown action"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(self._serialize_cart(request))

    def patch(self, request: Request) -> Response:
        """Установить точное количество: {product_id, quantity}"""
        raw_id = request.data.get("product_id")
        if raw_id is None:
            return Response({"detail": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        raw_qty = request.data.get("quantity")
        if raw_qty is None:
            return Response({"detail": "quantity is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product_id = int(raw_id)
            qty = int(raw_qty)
        except (TypeError, ValueError):
            return Response({"detail": "product_id and quantity must be int"}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, id=product_id, is_active=True)
        cart = Cart(request)

        current = cart.get_quantity(product)
        delta = qty - current
        if delta != 0:
            cart.change_quantity(product, delta)

        return Response(self._serialize_cart(request))

    def delete(self, request: Request) -> Response:
        """Очистить корзину"""
        Cart(request).clear()
        return Response(status=status.HTTP_204_NO_CONTENT)
