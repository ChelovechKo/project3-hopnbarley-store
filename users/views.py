from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm


class UserCreateView(CreateView):
    '''Регистрация пользователя'''
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


class HomeView(TemplateView):
    '''Домашняя страница'''
    template_name = 'users/home.html'