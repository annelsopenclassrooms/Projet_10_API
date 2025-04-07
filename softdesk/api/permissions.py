from rest_framework import permissions


class IsAuthorOrContributor(permissions.BasePermission):
    def has_object_permission(self, request, obj):
        return obj.author == request.user
