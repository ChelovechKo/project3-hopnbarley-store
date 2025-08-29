from django.urls import path
from .views import ProductDetailView, ProductListView


app_name = 'products'


urlpatterns = [
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/', ProductListView.as_view(), name='product-list'),
]