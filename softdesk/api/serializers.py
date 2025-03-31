from rest_framework.serializers import ModelSerializer
 
from authentication.models import User
from api.models import Project, Contributor, Issue, Comment

from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from .models import Project


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'date_of_birth', 'can_be_contacted', 'can_data_be_shared']


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'date_of_birth', 'can_be_contacted', 'can_data_be_shared']
        extra_kwargs = {
            'password': {'write_only': True},  # Masquer le mot de passe dans la réponse
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # Hachage du mot de passe
        return super().create(validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'type', 'author', 'created_time']
        extra_kwargs = {
            'author': {'read_only': True},  # Empêche la modification via l'API
            'created_time': {'read_only': True},
        }


class ContributorSerializer(ModelSerializer):
 
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project']

class IssueSerializer(ModelSerializer):
 
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'project', 'author', 'assignee', 'priority', 'tag', 'status', 'created_time']

class CommentSerializer(ModelSerializer):
 
    class Meta:
        model = Comment
        fields = ['id', 'description', 'issue', 'author', 'created_time']