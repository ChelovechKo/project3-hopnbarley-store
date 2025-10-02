from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.response import Response

from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer
from config.permissions import IsOwner
from orders.cart import Cart
from products.models import Product
from config.permissions import IsAuthenticatedOrSessionForCart


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

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items", "items__product")

    def get_serializer_class(self):
        return OrderCreateSerializer if self.action == "create" else OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartView(APIView):
    permission_classes = [IsAuthenticatedOrSessionForCart]

    def get(self, request):
        cart = Cart(request)
        items = []
        total = cart.get_total_price()
        for it in cart:
            items.append({
                "product": it["product"].id,
                "name": it["product"].name,
                "price": str(it["price"]),
                "quantity": it["quantity"],
                "total_price": str(it["total_price"]),
            })
        return Response({"items": items, "total": str(total)})

    def post(self, request):
        """Добавить/изменить позицию: {product_id, action: increase|decrease|remove}"""
        product_id = int(request.data.get("product_id"))
        action = request.data.get("action", "increase")
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
        return self.get(request)

    def patch(self, request):
        """Установить точное количество: {product_id, quantity}"""
        product_id = int(request.data.get("product_id"))
        qty = int(request.data.get("quantity"))
        product = get_object_or_404(Product, id=product_id, is_active=True)
        cart = Cart(request)

        # нормализуем до нужного количества
        current = cart.get_quantity(product)
        cart.change_quantity(product, qty - current)
        return self.get(request)

    def delete(self, request):
        """Очистить корзину"""
        cart = Cart(request)
        cart.clear()
        return Response(status=status.HTTP_204_NO_CONTENT)
