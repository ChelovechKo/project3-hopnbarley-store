from rest_framework.permissions import BasePermission, SAFE_METHODS
from typing import Any
from rest_framework.request import Request


class IsOwner(BasePermission):
    """Доступ к объекту только владельцу"""
    def has_object_permission(self, request: Request, view: Any, obj: Any) -> bool:
        user_id = getattr(getattr(obj, "user", None), "id", None)
        return user_id == getattr(request.user, "id", None)


class IsOwnerOrReadOnly(BasePermission):
    """Чтение всем, изменение только владельцу"""
    def has_object_permission(self, request: Request, view: Any, obj: Any) -> bool:
        if request.method in SAFE_METHODS:
            return True
        user_id = getattr(getattr(obj, "user", None), "id", None)
        return user_id == getattr(request.user, "id", None)


class IsAuthenticatedOrSessionForCart(BasePermission):
    """Для корзины: либо JWT-пользователь, либо активная сессия."""
    def has_permission(self, request: Request, view: Any) -> bool:
        return request.user.is_authenticated or request.session.session_key is not None
