# Create your views here.

from authentication.models import User
from api.models import Project, Contributor, Issue, Comment
from api.permissions import IsAuthorOrContributor, IsAuthor
from django.db.models import Q

from .serializers import (
    UserSerializer,
    ProjectSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer,
)

from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied


class UserAPIViewset(ModelViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        # Returns only the logged-in user for non-admins
        return User.objects.filter(id=user.id)

    def list(self, request, *args, **kwargs):
        # Only admins can see the full list
        if not request.user.is_superuser:
            raise PermissionDenied("Seuls les administrateurs peuvent voir la liste des utilisateurs.")
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class ProjectAPIViewset(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrContributor]

    def perform_create(self, serializer):
        try:
            # Save the project with the current user as the author
            project = serializer.save(author=self.request.user)
            # Add the author as a contributor
            Contributor.objects.create(project=project, user=self.request.user)
        except IntegrityError:
            raise ValidationError("A project with this name already exists.")

    def get_queryset(self):
        return Project.objects.filter(
            Q(author=self.request.user) | Q(contributors__user=self.request.user)
        ).distinct()


class ContributorAPIViewset(ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get contributors where the user is either the contributor or the project author
        return Contributor.objects.filter(
            Q(user=self.request.user) | Q(project__author=self.request.user)
        )

    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        # Check if the requesting user is the author of the project
        if project.author != self.request.user:
            raise PermissionDenied("Seul l'auteur du projet peut ajouter un contributeur.")
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        contributor = self.get_object()
        # Check if the requesting user is the author of the project
        if contributor.project.author != request.user:
            raise PermissionDenied("Seul l'auteur du projet peut supprimer un contributeur.")
        return super().destroy(request, *args, **kwargs)
        
class IssueAPIViewset(ModelViewSet):
    serializer_class = IssueSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only the issues from projects where the user is a contributor
        return Issue.objects.filter(
            project__contributors__user=self.request.user
        ).distinct()

    def perform_create(self, serializer):
        # Check before saving
        project = serializer.validated_data['project']
        if not project.contributors.filter(user=self.request.user).exists():
            raise PermissionDenied("Vous n'êtes pas contributeur de ce projet")

        # Automatic assignment of the author
        serializer.save(author=self.request.user)


class CommentAPIViewset(ModelViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self):
        # Only the comments from issues where the user is a contributor
        return Comment.objects.filter(
            issue__project__contributors__user=self.request.user
        ).distinct()

    def perform_create(self, serializer):
        # Check before saving
        issue = serializer.validated_data['issue']
        if not issue.project.contributors.filter(user=self.request.user).exists():
            raise PermissionDenied("Vous n'êtes pas contributeur de ce projet")

        # Automatic assignment of the author
        serializer.save(author=self.request.user)

class WhoAmIView(APIView):
    permission_classes = [IsAuthenticated]  # Requires a valid token

    def get(self, request):
        return Response({
            "user_id": request.user.id,
            "username": request.user.username,
        })