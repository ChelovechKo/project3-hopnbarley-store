from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from products.models import Category, Product, Review


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    fields = ('user', 'rating', 'head_comment', 'comment', 'create_at')
    readonly_fields = ('create_at',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]

    list_display = (
        'image_thumb', 'id', 'name', 'category', 'price', 'is_active', 'stock',
        'reviews_count', 'reviews_link', 'create_at', 'update_at',
    )
    list_filter = ('category', 'is_active', 'create_at', 'update_at', 'price')
    search_fields = ('name', 'description', 'slug', 'category__name')
    prepopulated_fields = {'slug': ('name',)}

    @admin.display(description='Image')
    def image_thumb(self, obj: Product) -> str:
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;" />', obj.image.url)
        return '—'

    @admin.display(description='Reviews')
    def reviews_count(self, obj: Product) -> int:
        return obj.reviews.count()

    @admin.display(description='Open reviews')
    def reviews_link(self, obj: Product) -> str:
        url = reverse('admin:products_review_changelist')
        query = urlencode({'product__id__exact': obj.pk})
        return format_html('<a href="{}?{}">Open ({})</a>', url, query, obj.reviews.count())


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'parent', 'create_at', 'update_at')
    list_filter = ('parent', 'create_at', 'update_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'rating', 'head_comment', 'create_at')
    list_filter = ('rating', 'product', 'user', 'create_at')
    search_fields = (
        'head_comment', 'comment',
        'product__name',
        'user__username', 'user__email',
    )
    raw_id_fields = ('product', 'user')
