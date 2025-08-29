from django.urls import path
from .views import ProductDetailView


app_name = 'products'


urlpatterns = [
    path('products/<slug:slug>', ProductDetailView.as_view(), name='product'),
]