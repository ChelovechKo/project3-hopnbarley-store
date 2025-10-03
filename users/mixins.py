from typing import Any, cast
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse
from django.views import View


class LoginRequiredMixin(View):
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('users:login')
        resp = super().dispatch(request, *args, **kwargs)
        return cast(HttpResponse, resp)
