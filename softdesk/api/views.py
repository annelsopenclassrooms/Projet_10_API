from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from authentication.models import User
from api.models import Project, Contributor, Issue, Comment
from api.serializers import UserSerializer, ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView


from rest_framework import generics, permissions

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .permissions import IsAuthorOrContributor




from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import (
    UserSerializer,
    ProjectSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer,

)
from .permissions import IsAuthorOrContributor, IsProjectContributor
from rest_framework import status
from rest_framework.exceptions import PermissionDenied




from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class UserAPIViewset(ModelViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        # Retourne uniquement l'utilisateur connecté pour les non-admins
        return User.objects.filter(id=user.id)

    def list(self, request, *args, **kwargs):
        # Seuls les admins peuvent voir la liste complète
        if not request.user.is_superuser:
            raise PermissionDenied("Seuls les administrateurs peuvent voir la liste des utilisateurs.")
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # Création classique (à adapter selon vos besoins de permissions)
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
        # Save the project with the current user as the author
        project = serializer.save(author=self.request.user)
        # Add the author as a contributor
        Contributor.objects.create(project=project, user=self.request.user)

    def get_queryset(self):
        return Project.objects.filter(author=self.request.user)     


class WhoAmIView(APIView):
    permission_classes = [IsAuthenticated]  # Nécessite un token valide

    def get(self, request):
        return Response({
            "user_id": request.user.id,
            "username": request.user.username,
        })


class ContributorAPIViewset(ModelViewSet):

    serializer_class = ContributorSerializer

    def get_queryset(self):

        return Contributor.objects.all()


class IssueAPIViewset(ModelViewSet):
    serializer_class = IssueSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Seules les issues des projets où l'utilisateur est contributeur
        return Issue.objects.filter(
            project__contributors__user=self.request.user
        ).distinct()

    def perform_create(self, serializer):
        # Vérification finale avant sauvegarde
        project = serializer.validated_data['project']
        if not project.contributors.filter(user=self.request.user).exists():
            raise PermissionDenied("Vous n'êtes pas contributeur de ce projet")

        # Assignation automatique de l'auteur
        serializer.save(author=self.request.user)


class CommentAPIViewset(ModelViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self): 
        # Seules les commentaires des issues où l'utilisateur est contributeur
        return Comment.objects.filter(
            issue__project__contributors__user=self.request.user
        ).distinct()

    def perform_create(self, serializer):
        # Vérification finale avant sauvegarde
        issue = serializer.validated_data['issue']
        if not issue.project.contributors.filter(user=self.request.user).exists():
            raise PermissionDenied("Vous n'êtes pas contributeur de ce projet")

        # Assignation automatique de l'auteur
        serializer.save(author=self.request.user)

