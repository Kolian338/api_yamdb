from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.auth
                    and (request.user.role == 'admin'
                         or request.user.is_superuser)))


class IsModerator(BasePermission):
    ...


class IsAdmin(BasePermission):
    """
    Юзер не аноним с ролью равной admin.
    """

    def has_permission(self, request, view):
        return (request.auth and request.user.role == 'admin'
                or request.user.is_superuser)
