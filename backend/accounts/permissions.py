from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

from .models import UserRole


class PasswordChanged(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.must_change_password:
            raise PermissionDenied(
                {"code": "password_change_required", "detail": "Password change required."}
            )
        return bool(request.user.is_authenticated)


class AdministratorOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and not request.user.must_change_password
            and request.user.role == UserRole.ADMINISTRATOR
        )
