from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path, include
from django.conf.urls.static import static
from config import settings
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from products.api import ProductViewSet, ProductReviewView
from orders.api import OrderViewSet, CartView
from users.api import RegisterView

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"orders", OrderViewSet, basename="order")

urlpatterns = [
    path('', RedirectView.as_view(url='/products/', permanent=False)),
    path('products/', include(('products.urls', 'products'), namespace='products')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('orders/', include('orders.urls', namespace='orders')),

    # --- REST API ---
    path("api/", include(router.urls)),
    path("api/cart/", CartView.as_view(), name="api-cart"),
    path("api/products/<int:pk>/reviews/", ProductReviewView.as_view(), name="api-product-reviews"),

    # users & JWT
    path("api/users/register/", RegisterView.as_view(), name="api-register"),
    path("api/users/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/users/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # OpenAPI/Swagger
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
