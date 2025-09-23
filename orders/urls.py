from django.urls import path
from orders.views import cart_change, cart_remove, cart_detail

app_name = 'orders'

urlpatterns = [
    path('cart/change/<int:product_id>/', cart_change, name='cart_change'),
    path('cart/', cart_detail, name='cart_detail'),
]