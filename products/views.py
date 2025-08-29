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
        context['reviews'] = Review.objects.filter(product=self.object)
        return context


class ProductListView(ListView):
    """Домашняя страница с каталогом товаров"""
    queryset = Product.objects.filter(is_active=True)
    context_object_name = 'products'
    template_name = 'products/product-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class GuidesRecipesView(TemplateView):
    template_name = 'guides-recipes.html'
