from rest_framework import permissions
from .models import USER, MODERATOR, ADMIN

class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == USER
        )

    def has_object_permission(self, request, view, obj):
        return True # доделать


class ModeratorPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == MODERATOR
        )

    def has_object_permission(self, request, view, obj):
        return True # доделать


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.role == ADMIN
                 or request.user.is_superuser)
        )
