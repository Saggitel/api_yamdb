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


class OwnerUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method != 'PUT'

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated and request.user.role == ADMIN
            )
        )


class IsUserAdminModeratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role == MODERATOR
            or request.user.role == ADMIN
        )