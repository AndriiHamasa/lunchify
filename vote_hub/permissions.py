from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrAuthenticatedForReading(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.method in SAFE_METHODS
        ) or request.user.is_superuser
