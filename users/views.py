from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm
from .mixins import LoginRequiredMixin


class UserCreateView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'users/account.html'
