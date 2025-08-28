from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from . import views

app_name = 'users'

urlpatterns = [
    # TODO: wrong success url
    path('register/', views.UserCreateView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html',
                                     next_page=reverse_lazy('users:home'),
                                     ), name='login'),
    path('home/', views.HomeView.as_view(), name='home'),
]