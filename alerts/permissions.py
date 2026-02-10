"""
Permission file to declare who can resolve alerts.
"""
from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow only admins to modify objects."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.role == "ADMIN"