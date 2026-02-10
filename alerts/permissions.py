"""
Permission file to declare who can resolve alerts.
"""
from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow only admins to modify objects."""

    def has_permission(self, request, view):
        return request.user and request.user.role == "ADMIN"