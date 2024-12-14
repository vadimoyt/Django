from rest_framework import permissions

class IsTrainer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_athenticated:
            return request.user.role == 'trainer'
        return False


class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_athenticated:
            return request.user.role == 'client'
        return False