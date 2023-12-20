from rest_framework.permissions import (BasePermission, SAFE_METHODS)


class ReadOnly(BasePermission):
    """Только чтение."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsAdmin(BasePermission):
    """
    Не аноним. С ролью admin или признак суперюзера.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and request.user.role == 'admin')


class IsSuperUser(BasePermission):
    """
    Все действия для суперюзера.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser


class IsAuthenticatedUser(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                )

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user)


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'moderator'


class IsAnonymous(BasePermission):
    """Разрешено только чтение анониму."""

    def has_permission(self, request, view):
        return not request.auth and request.method in SAFE_METHODS
