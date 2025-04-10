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


class IsIssueAuthorOrReadOnly(permissions.BasePermission):
    """
    Autorise tout utilisateur contributeur à lire.
    Autorise uniquement l'auteur à modifier ou supprimer.
    """
    def has_object_permission(self, request, view, obj):
        # Lecture seule autorisée pour tous les contributeurs
        if request.method in permissions.SAFE_METHODS:
            return obj.project.contributors.filter(user=request.user).exists()

        # Modification / suppression uniquement par l'auteur de l'issue
        return obj.author == request.user
    

class IsCommentAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.issue.project.contributors.filter(user=request.user).exists()
        return obj.author == request.user


class IsProjectAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.author == request.user or obj.contributors.filter(user=request.user).exists()
        return obj.author == request.user