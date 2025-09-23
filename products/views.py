from django.views.generic import DetailView, ListView, TemplateView
from products.models import Product, Review, Category
from django.db.models import Avg, Q
from config.settings import PRODUCTS_QUERY_MAP
from orders.cart import Cart


class ProductDetailView(DetailView):
    """Страница с описанием товара"""
    slug_field = 'slug'
    model = Product
    template_name = 'products/product-details.html'

    def get_object(self, queryset=None):
        return Product.objects.get(slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(product=self.object)

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
    paginate_by = 1
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


class GuidesRecipesView(TemplateView):
    template_name = 'guides-recipes.html'
