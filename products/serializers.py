from rest_framework import serializers
from typing import ClassVar

from products.models import Product, Category, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "parent")


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = (
            "id", "name", "slug", "description", "price",
            "category", "image", "stock", "is_active", "create_at"
        )


class ReviewSerializer(serializers.ModelSerializer):
    user: ClassVar[serializers.Field] = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ("id", "rating", "head_comment", "comment", "user", "create_at")
