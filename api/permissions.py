# api/permissions.py
from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Allows access only to owners (user.role == 'owner').
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'owner')

class IsCaretaker(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'caretaker')

class IsTenant(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'tenant')

class IsOwnerOrCaretaker(permissions.BasePermission):
    """
    Allows access if user is owner OR caretaker.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in ('owner','caretaker'))

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Read-only access for everyone; write if owner of the object.
    Assumes the object has `owner` attribute (FK).
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return hasattr(obj, 'owner') and obj.owner == request.user
