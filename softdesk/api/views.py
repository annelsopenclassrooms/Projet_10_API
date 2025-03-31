from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from authentication.models import User
from api.models import Project, Contributor, Issue, Comment
from api.serializers import UserSerializer, ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer, RegisterSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from .serializers import RegisterSerializer

from rest_framework import generics, permissions

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .permissions import IsAuthorOrContributor, IsProjectContributor


class UserAPIViewset(ModelViewSet):

    serializer_class = UserSerializer

    def get_queryset(self):

        return User.objects.all()
    

class RegisterView(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer


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