from rest_framework.permissions import (BasePermission, SAFE_METHODS)


class IsAdminOrSuperUser(BasePermission):
    """
    Не аноним. С ролью admin или признак суперюзера.
    """

    def has_permission(self, request, view):
        return (request.auth
                and request.user.role == 'admin'
                or request.user.is_superuser)


class IsModeratorOrAuthenticatedUser(BasePermission):
    """
    Роль user может все читать и редактировать/удалять только своё.
    Роль moderator может делать всё.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user.role in ('user', 'moderator')
        )

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'user':
            return obj.author == request.user
        return request.user.role == 'moderator'


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser or request.method in SAFE_METHODS


class IsAnonymous(BasePermission):
    """Разрешено только чтение анониму."""

    def has_permission(self, request, view):
        return not request.auth and request.method in SAFE_METHODS
