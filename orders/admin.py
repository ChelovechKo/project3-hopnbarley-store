from django.contrib import admin
from orders.models import Order, OrderItem


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInLine]
    list_display = ('id', 'user', 'create_at', 'update_at', 'total_price')
    list_filter = ('user', 'create_at', 'update_at')
    search_fields = ('user__username', 'user__email')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price')
    list_filter = ('order', 'product')
    search_fields = ('order__user__username', 'order__user__email')
