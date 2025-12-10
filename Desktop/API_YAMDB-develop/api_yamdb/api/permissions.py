from rest_framework import permissions


class OnlyAdmin(permissions.BasePermission):
    """Только администратор."""
    def has_permission(self, request, view):
        return request.user.role == 'admin' or request.user.is_superuser


class AdminOrMeOnly(permissions.BasePermission):
    """Только админ и зарегестрированный пользователь для /me."""
    def has_permission(self, request, view):
        if view.action == 'me':
            return request.user.is_authenticated
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Админу - всё.
    Остальным - только чтение (GET, HEAD, OPTIONS).
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    """
    Чтение - всем.
    Создание - аутентифицированным.
    Изменение/удаление - Автор, Модератор, Админ.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
