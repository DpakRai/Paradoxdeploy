from rest_framework.permissions import BasePermission

class UserPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            return False

        if view.action == 'create':
            return True
        elif view.action == 'list':
            return request.user.is_staff
        elif view.action == 'update':
            return True
        elif view.action == 'delete':
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        elif request.user == obj:
            return True