from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, obj):

        return bool(request.user == obj.user)
