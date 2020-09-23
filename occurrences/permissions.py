from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class IsAuthor(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to see and edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        return obj.author == request.user


class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        return obj.author == request.user


class DontAllowCreateAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Grants permission if the user being created is not admin and we're not authenticated,
        Denys permission if the user being created is admin and we're not authenticated with an admin account
        """
        if request.POST.get('is_staff') or request.POST.get('is_superuser'):
            return bool(request.user and request.user.is_superuser)
        return True

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
