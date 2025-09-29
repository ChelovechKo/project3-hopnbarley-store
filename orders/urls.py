from django.urls import path
from orders.views import cart_change, checkout, cart_detail, order_detail

app_name = 'orders'

urlpatterns = [
    path('cart/change/<int:product_id>/', cart_change, name='cart_change'),
    path('cart/', cart_detail, name='cart_detail'),
    path('checkout/', checkout, name='checkout'),
    path('order/<int:pk>/', order_detail, name='order_detail'),
]
