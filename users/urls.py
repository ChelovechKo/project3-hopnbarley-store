from django.urls import path,reverse_lazy
from django.contrib.auth.views import LoginView

from .views import UserCreateView, HomeView, AccountView

app_name = 'users'

urlpatterns = [
    # TODO: wrong success url
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html',
                                     next_page=reverse_lazy('users:home'),
                                     ), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('account/', AccountView.as_view(), name='account'),
]