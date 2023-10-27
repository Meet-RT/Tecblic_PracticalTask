from rest_framework import permissions


class Is_AdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_admin)


class Is_Solution_ProviderUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_solution_provider_user)


class Is_Solution_SeekerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_solution_seeker_user)

