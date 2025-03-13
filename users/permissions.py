from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """Allows access only to Admin users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsManager(permissions.BasePermission):
    """Allows access only to Manager users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'manager'

class IsCustomer(permissions.BasePermission):
    """Allows access only to Customer users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'customer'
    

class IsAdminOrManager(permissions.BasePermission):
    """Allows access only to Customer users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role  in ['admin','manager']
    


class IsAdminOrCustomer(permissions.BasePermission):
    """Allows access only to Customer users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'customer'    
