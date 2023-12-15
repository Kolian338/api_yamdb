from rest_framework.permissions import (BasePermission, SAFE_METHODS,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly,
                                        )


class IsAdminOrSuperUserDjango(BasePermission):
    """
    Не аноним. С ролью admin или суперюзер.
    """

    def has_permission(self, request, view):
        return (request.auth and
                request.user.role == 'admin' or
                request.user.is_superuser)


class IsModeratorOrAuthenticatedUser(BasePermission):
    """
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user.role in ('user', 'moderator')
        )

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'moderator':
            return True
        if request.user.role == 'user':
            return obj.author == request.user


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser or request.method in SAFE_METHODS


class IsAnonymous(BasePermission):
    """Разрешено чтение анониму."""

    def has_permission(self, request, view):
        return not request.auth and request.method in SAFE_METHODS
