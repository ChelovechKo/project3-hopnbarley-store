from typing import Any, Dict
from django.views.generic import CreateView, TemplateView, UpdateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator

from users.forms import UserRegistrationForm, UserUpdateForm
from users.mixins import LoginRequiredMixin
from users.models import User


class UserCreateView(CreateView):
    """Регистрация пользователя"""
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


class AccountView(LoginRequiredMixin, TemplateView):
    """Список заказов и информация об аккаунте"""
    template_name = 'users/account.html'
    allow_empty = True

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        assert self.request.user.is_authenticated
        user = self.request.user

        context['form'] = UserUpdateForm(instance=user)

        orders_qs = user.orders.order_by('-create_at')
        paginator = Paginator(orders_qs, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['is_paginated'] = page_obj.has_other_pages()
        context['paginator'] = paginator
        context['orders'] = page_obj.object_list
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление информации в аккаунте"""
    queryset = User.objects.all()
    form_class = UserUpdateForm
    success_url = reverse_lazy('users:account')
