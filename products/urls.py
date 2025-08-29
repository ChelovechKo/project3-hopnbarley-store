from django.urls import path
from .views import ProductDetailView, ProductListView, GuidesRecipesView


app_name = 'products'


urlpatterns = [
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('guides-recipes/', GuidesRecipesView.as_view(), name='guides-recipes'),
]