from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from products.models import JournalizedModel


class OrderStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    PAID = 'paid', 'Paid'
    SHIPPED = 'shipped', 'Shipped'
    DELIVERED = 'delivered', 'Delivered'
    CANCELLED = 'cancelled', 'Cancelled'


class Order(JournalizedModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='orders', null=True, blank=True)
    status = models.CharField(max_length=20, choices=OrderStatus, default=OrderStatus.PENDING)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    shipping_address = models.TextField(max_length=200)

    def __str__(self):
        return f"Order {self.id}"

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-create_at']


class OrderItem(JournalizedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"OrderItem {self.id}"

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        ordering = ['-create_at']
