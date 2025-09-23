from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product
from django.views.generic import TemplateView
from orders.cart import Cart


class CartDetail(TemplateView):
    template_name = 'orders/cart_detail.html'


@require_POST
def cart_change(request, product_id):
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
    cart = Cart(request)
    cart.remove(product)
    return redirect('orders:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'orders/cart_detail.html', {'cart': cart})
