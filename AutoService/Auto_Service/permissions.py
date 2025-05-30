from rest_framework.permissions import BasePermission



class IsClient(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'client')

class IsMaster(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'master')
