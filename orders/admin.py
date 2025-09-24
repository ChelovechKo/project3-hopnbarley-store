from django.contrib import admin
from orders.models import OrderItem


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInLine]
    list_display = ('id', 'user', 'created_at', 'updates_at', 'total_price')
    list_filter = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price')
    list_filter = ('order', 'product')
    search_fields = ('order__user__username', 'order__user__email')
