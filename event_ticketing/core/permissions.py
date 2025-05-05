from rest_framework import permissions

class IsOrganizer(permissions.BasePermission):
    """
    Custom permission to only allow organizers to access a view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_organizer()

class IsUser(permissions.BasePermission):
    """
    Custom permission to only allow regular users to access a view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_user()

class IsOrganizerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow organizers to edit, but read-only for others.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_organizer()