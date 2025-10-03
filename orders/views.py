from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from django.db import transaction, models
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model

from orders.cart import Cart
from orders.forms import CheckoutForm
from orders.models import Order, OrderItem, OrderStatus
from products.models import Product, Review



User = get_user_model()


class CartDetail(TemplateView):
    template_name = 'orders/cart_detail.html'


@require_POST
def cart_change(request: HttpRequest, product_id: int) -> HttpResponseRedirect:
    """Изменение количества товара в корзине"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)
    action = request.POST.get('action')

    stock = max(int(product.stock or 0), 0)
    current_qty = cart.get_quantity(product)

    if action == 'increase' and stock >= current_qty + 1:
        cart.change_quantity(product, 1)
    elif action == 'decrease':
        cart.change_quantity(product, -1)
    elif action == 'remove':
        cart.remove(product)

    next_url = request.GET.get('next')
    return redirect(next_url or 'orders:cart_detail')


def cart_remove(request: HttpRequest, product: Product) -> HttpResponseRedirect:
    """Очистка корзины"""
    cart = Cart(request)
    cart.remove(product)
    return redirect('orders:cart_detail')


def cart_detail(request: HttpRequest) -> HttpResponse:
    """Отображение корзины"""
    cart = Cart(request)
    return render(request, 'orders/cart_detail.html', {'cart': cart})


def checkout(request: HttpRequest) -> HttpResponse:
    """Оформление заказа"""
    cart = Cart(request)
    assert request.user.is_authenticated
    user = request.user

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            shipping_address = f"{cd['city']}, {cd['address']}"
            status = OrderStatus.PAID if cd['payment_method'] != 'cod' else OrderStatus.PENDING

            with transaction.atomic():
                # Блокируем продукты, которые есть в корзине
                items = list(cart)
                product_ids = [i['product'].id for i in items]
                products_locked = (
                    Product.objects.select_for_update()
                    .filter(id__in=product_ids, is_active=True)
                )
                products_by_id = {p.id: p for p in products_locked}

                # Валидация остатков
                for it in items:
                    p = products_by_id.get(it['product'].id)
                    if not p or it['quantity'] <= 0 or it['quantity'] > p.stock:
                        messages.error(request, f"Not enough stock for {it['product'].name}.")
                        return redirect('orders:cart_detail')

                # Списание остатков
                for it in items:
                    p = products_by_id[it['product'].id]
                    p.stock = models.F('stock') - it['quantity']
                    p.save(update_fields=['stock'])

                # Создание ордера в БД
                order = Order.objects.create(
                    user=user,
                    status=status,
                    total_price=cart.get_total_price(),
                    shipping_address=shipping_address,
                )

                # Добавление продуктов в ордер в БД
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
                recipient = [user.email]
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient)

            return render(request, 'orders/checkout_success.html', {'order': order})
    else:
        form = CheckoutForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone,
            'city': user.city,
            'address': user.address,
        })
    return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})


def order_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """Страница с деталями заказа"""
    assert request.user.is_authenticated
    user = request.user
    order = get_object_or_404(Order, pk=pk, user=user)
    items = order.items.select_related('product')

    # User's reviews
    product_ids = items.values_list('product_id', flat=True)
    reviews = Review.objects.filter(user=user, product_id__in=product_ids)
    reviews_by_product = {r.product_id: r for r in reviews}

    return render(request, 'orders/order_detail.html', {
        'order': order,
        'items': items,
        'reviews_by_product': reviews_by_product,
    })
