from rest_framework import permissions
from users.models import ADMIN, MODERATOR, USER


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == USER
        )

    def has_object_permission(self, request, view, obj):
        return True  # доделать


class ModeratorPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == MODERATOR
        )

    def has_object_permission(self, request, view, obj):
        return True  # доделать


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.role == ADMIN
                 or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return True


class OwnerOrAdminPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and (request.user.role == ADMIN
                 or request.user.is_superuser
                 or obj == request.user)
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == ADMIN
        )
