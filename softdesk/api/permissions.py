from rest_framework import permissions


class IsAuthorOrContributor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or obj.contributors.filter(user=request.user).exists()
        )


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
