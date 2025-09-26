from django.views.generic import CreateView, TemplateView, UpdateView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, UserUpdateForm
from .mixins import LoginRequiredMixin
from .models import User


class UserCreateView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'users/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserUpdateForm(instance=self.request.user)
        context['orders'] = self.request.user.orders.all()
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    queryset = User.objects.all()
    form_class = UserUpdateForm
    success_url = reverse_lazy('users:account')
