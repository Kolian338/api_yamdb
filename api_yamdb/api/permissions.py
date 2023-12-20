from rest_framework.permissions import (BasePermission, SAFE_METHODS)


class IsAdminOrSuperUser(BasePermission):
    """
    Не аноним. С ролью admin или признак суперюзера.
    """

    def has_permission(self, request, view):
        return (request.auth
                and request.user.role == 'admin'
                or request.user.is_superuser)


class IsAdminModeratorOrAuthenticatedUser(BasePermission):
    """
    Читать могут все.
    Роль user может редактировать/удалять только своё.
    Роль admin/moderator может делать всё.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
                request.method in SAFE_METHODS
                or obj.author == request.user
                or request.user.role == 'moderator'
                or request.user.role == 'admin'
        )


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_superuser)


class IsAnonymous(BasePermission):
    """Разрешено только чтение анониму."""

    def has_permission(self, request, view):
        return not request.auth and request.method in SAFE_METHODS
