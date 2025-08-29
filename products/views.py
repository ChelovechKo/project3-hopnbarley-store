from django.shortcuts import render
from django.views.generic import ListView, DetailView
from products.models import Product, Review

class ProductDetailView(DetailView):
    slug_field = 'slug'
    model = Product
    template_name = 'products/product-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(product=self.object)
        return context