from django.urls import path
from .views import ProductDetailView, ProductListView, GuidesRecipesView, Community, Resources, Contact, FAQ, License, leave_review


app_name = 'products'


urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('community/', Community.as_view(), name='community'),
    path('resources/', Resources.as_view(), name='resources'),
    path('contact/', Contact.as_view(), name='contact'),
    path('faq/', FAQ.as_view(), name='faq'),
    path('license/', License.as_view(), name='license'),
    path('guides-recipes/', GuidesRecipesView.as_view(), name='guides-recipes'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<slug:slug>/review/', leave_review, name='leave_review'),

]
