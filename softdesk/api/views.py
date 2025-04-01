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

from .permissions import IsAuthorOrContributor, IsProjectContributor




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
        # Associe automatiquement l'utilisateur connecté comme auteur
        serializer.save(author=self.request.user)
            
    def get_queryset(self):
        return Project.objects.filter(author=self.request.user)     


class WhoAmIView(APIView):
    permission_classes = [IsAuthenticated]  # Nécessite un token valide

    def get(self, request):
        return Response({
            "user_id": request.user.id,
            "username": request.user.username,
        })


#a supprimer
class ContributorAPIViewset(ModelViewSet):

    serializer_class = ContributorSerializer

    def get_queryset(self):

        return Contributor.objects.all()
    



class IssueAPIViewset(ModelViewSet):

    serializer_class = IssueSerializer

    def get_queryset(self):

        return Issue.objects.all()

class CommentAPIViewset(ModelViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self):

        return Comment.objects.all()
    


class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsProjectContributor]

    def get_queryset(self):
        return Contributor.objects.filter(project_id=self.kwargs['project_id'])

    def perform_create(self, serializer):
        serializer.save(project_id=self.kwargs['project_id'])

class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsProjectContributor]

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs['project_id'])

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            project_id=self.kwargs['project_id']
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsProjectContributor]

    def get_queryset(self):
        return Comment.objects.filter(issue_id=self.kwargs['issue_id'])

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            issue_id=self.kwargs['issue_id']
        )

# class RegisterViewSet(viewsets.GenericViewSet):
#     serializer_class = RegisterSerializer
#     queryset = User.objects.all()

#     def create(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=201)