from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from authentication.models import User
from api.models import Project
from api.serializers import UserSerializer, ProjectSerializer


class UserAPIViewset(ModelViewSet):

    serializer_class = UserSerializer

    def get_queryset(self):

        return User.objects.all()

class ProjectAPIViewset(ModelViewSet):

    serializer_class = ProjectSerializer

    def get_queryset(self):

        return Project.objects.all()