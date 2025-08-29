from django.views.generic import DetailView
from products.models import Product, Review


class ProductDetailView(DetailView):
    slug_field = 'slug'
    model = Product
    template_name = 'products/product-details.html'

    def get_object(self, queryset=None):
        return Product.objects.get(slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(product=self.object)
        return context
