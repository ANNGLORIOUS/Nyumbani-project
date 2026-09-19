from rest_framework.permissions import BasePermission


def is_manager(user):
    return user.is_authenticated and (user.is_superuser or user.role in ('owner', 'agent', 'caretaker', 'admin'))


class CanManageProperty(BasePermission):
    def has_permission(self, request, view):
        return is_manager(request.user)


class IsPropertyOwnerOrAgent(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user or request.user.is_superuser:
            return True
        return request.user.role in ('agent', 'caretaker', 'admin') and obj.caretaker == request.user
