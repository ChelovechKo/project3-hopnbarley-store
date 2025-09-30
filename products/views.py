from django.shortcuts import redirect, get_object_or_404
from django.db.models import Avg, Q
from config.settings import PRODUCTS_QUERY_MAP
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from orders.cart import Cart
from django.views.generic import DetailView, ListView, TemplateView
from products.models import Product, Review, Category


class ProductDetailView(DetailView):
    """Страница с описанием товара"""
    slug_field = 'slug'
    model = Product
    template_name = 'products/product-details.html'

    def get_object(self, queryset=None):
        return Product.objects.get(slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(product=self.object)[:3]

        cart = Cart(self.request)
        raw = cart.cart.get(str(self.object.id), {})
        context['item'] = {
            'quantity': raw.get('quantity', 0),
            'price': raw.get('price'),
        }
        return context


class ProductListView(ListView):
    """Домашняя страница с каталогом товаров"""
    context_object_name = 'products'
    template_name = 'products/product-list.html'
    paginate_by = 9
    allow_empty = True

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True) \
            .select_related('category') \
            .annotate(avg_rating=Avg('reviews__rating'))

        # filter by category
        categories = self.request.GET.get('categories', None)
        if categories:
            qs = qs.filter(category__slug__in=categories.split(','))

        # search
        to_search = self.request.GET.get('q', None)
        if to_search:
            qs = qs.filter(
                Q(name__icontains=to_search) |
                Q(description__icontains=to_search)
            )

        # sort
        qs_key = self.request.GET.get('sort', 'new')
        qs = qs.order_by(PRODUCTS_QUERY_MAP[qs_key])

        return list(qs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        context['sort_options'] = [
            {'key': 'new', 'label': 'New'},
            {'key': 'price_asc', 'label': 'Price ascending'},
            {'key': 'price_desc', 'label': 'Price descending'},
            {'key': 'rating', 'label': 'Rating'}
        ]

        return context


@require_POST
@login_required
def leave_review(request, slug):
    """Создание отзыва на продукт"""
    product = get_object_or_404(Product, slug=slug)
    head_comment = request.POST.get('head_comment')
    comment = request.POST.get('comment')
    rating = int(request.POST.get('rating'))

    Review.objects.update_or_create(
        product=product,
        user=request.user,
        defaults={
            'rating': rating,
            'head_comment': head_comment,
            'comment': comment,
        }
    )

    order_id = int(request.POST.get('order_id'))
    if order_id:
        return redirect('orders:order_detail', pk=order_id)
    return redirect('products:product-detail', slug=product.slug)


class GuidesRecipesView(TemplateView):
    """Гайды и рецепты (Заглушка)"""
    template_name = 'guides-recipes.html'


class Community(TemplateView):
    """Сообщество (Заглушка)"""
    template_name = 'community.html'


class Resources(TemplateView):
    """Ресурсы (Заглушка)"""
    template_name = 'resources.html'


class Contact(TemplateView):
    """Контакты (Заглушка)"""
    template_name = 'contact.html'


class FAQ(TemplateView):
    """FAQ (Заглушка)"""
    template_name = 'faq.html'


class License(TemplateView):
    """Лиценция (Заглушка)"""
    template_name = 'license.html'
