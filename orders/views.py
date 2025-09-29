from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from django.db import transaction
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

from products.models import Product

from orders.cart import Cart
from orders.forms import CheckoutForm
from orders.models import Order, OrderItem, OrderStatus


class CartDetail(TemplateView):
    template_name = 'orders/cart_detail.html'


@require_POST
def cart_change(request, product_id):
    """Изменение количества товара в корзине"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    action = request.POST.get('action', 'increase')

    if action == 'increase':
        cart.change_quantity(product, 1)
    elif action == 'decrease':
        cart.change_quantity(product, -1)
    elif action == 'remove':
        cart.remove(product)
    else:
        pass

    next_url = request.GET.get('next')
    return redirect(next_url or 'orders:cart_detail')


def cart_remove(request, product):
    """Очистка корзины"""
    cart = Cart(request)
    cart.remove(product)
    return redirect('orders:cart_detail')


def cart_detail(request):
    """Отображение корзины"""
    cart = Cart(request)
    return render(request, 'orders/cart_detail.html', {'cart': cart})


def checkout(request):
    """Оформление заказа"""
    cart = Cart(request)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            shipping_address = f"{cd['city']}, {cd['address']}"
            status = OrderStatus.PAID if cd['payment_method'] != 'cod' else OrderStatus.PENDING

            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    status=status,
                    total_price=cart.get_total_price(),
                    shipping_address=shipping_address,
                )
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity'],
                    )
                order.save()
                cart.clear()

                subject = f"Order #{order.id} confirmation"
                message = (
                    f"Hello, {cd['first_name']}!\n\n"
                    f"Thank you for your order #{order.id}.\n"
                    f"Status: {order.status}\n"
                    f"Total: ${order.total_price}\n\n"
                )
                recipient = [request.user.email]
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient)

            return render(request, 'orders/checkout_success.html', {'order': order})
    else:
        form = CheckoutForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'phone': request.user.phone,
            'city': request.user.city,
            'address': request.user.address,
        })
    return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})


@login_required
def order_detail(request, pk):
    """Страница с деталями заказа"""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    items = order.items.select_related('product')

    return render(request, 'orders/order_detail.html', {
        'order': order,
        'items': items,
    })

