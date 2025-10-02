from django.conf import settings
from rest_framework.views import APIView
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from orders.models import OrderItem
from products.models import Product
from .models import Review as ReviewModel
from .serializers import ProductSerializer, ReviewSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    list=extend_schema(tags=["Products"], summary="Список товаров"),
    retrieve=extend_schema(tags=["Products"], summary="Детали товара"),
)
class ProductViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Product.objects.filter(is_active=True).select_related("category")
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filterset_fields = ["category", "price"]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "create_at"]

    def list(self, request, *args, **kwargs):
        # поддержка ?sort= из PRODUCTS_QUERY_MAP
        sort_key = request.query_params.get("sort", "new")
        sort_map = getattr(settings, "PRODUCTS_QUERY_MAP", {})
        if sort_key in sort_map:
            self.queryset = self.queryset.order_by(sort_map[sort_key])
        return super().list(request, *args, **kwargs)


class ProductReviewView(APIView):
    """GET — список отзывов; POST — создать (только после покупки)."""

    def get_permissions(self):
        return [AllowAny()] if self.request.method == "GET" else [IsAuthenticated()]

    @extend_schema(tags=["Reviews"], summary="Отзывы по продукту")
    def get(self, request, pk: int):
        qs = ReviewModel.objects.filter(product_id=pk).select_related("user")
        return Response(ReviewSerializer(qs, many=True).data)

    @extend_schema(tags=["Reviews"], summary="Создать отзыв (после покупки)")
    def post(self, request, pk: int):
        bought = OrderItem.objects.filter(
            order__user=request.user,
            product_id=pk,
            order__status__in=["paid", "delivered"]
        ).exists()
        if not bought:
            return Response({"detail": "Оставлять отзыв можно только после покупки."},
                            status=status.HTTP_403_FORBIDDEN)
        ser = ReviewSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save(user=request.user, product_id=pk)
        return Response(ser.data, status=status.HTTP_201_CREATED)
