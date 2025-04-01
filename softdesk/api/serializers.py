from rest_framework.serializers import ModelSerializer, ValidationError, CharField
 
from authentication.models import User
from api.models import Project, Contributor, Issue, Comment

from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from .models import Project

from datetime import timedelta
from django.utils.timezone import now
from rest_framework import status


class UserSerializer(ModelSerializer):
    password_confirm = CharField(write_only=True)  # Ajout du champ pour la confirmation du mot de passe

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password_confirm', 'date_of_birth', 'can_be_contacted', 'can_data_be_shared']
        extra_kwargs = {
            'password': {'write_only': True},  # Ne montre jamais le mot de passe en clair
            'id': {'read_only': False}  # Permet d'écrire l'id (re creation user apres suppression lors de la demo)
        }

    def validate(self, data):
        request = self.context.get('request')
        is_creation = request and request.method == 'POST'

        date_of_birth = data.get('date_of_birth')
        can_data_be_shared = data.get('can_data_be_shared', False)
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        # Vérification de la date de naissance uniquement à la création
        if is_creation and not date_of_birth:
            raise ValidationError({"date_of_birth": "La date de naissance est obligatoire lors de la création du compte."})

        # Vérification du mot de passe et de sa confirmation
        if password and password != password_confirm:
            raise ValidationError({"password_confirm": "Les mots de passe ne correspondent pas."})

        # Vérification de l'âge pour le partage des données
        if date_of_birth:  # Vérifier l'âge seulement si une date est fournie
            age = (now().date() - date_of_birth).days // 365
            if can_data_be_shared and age < 15:
                raise ValidationError({"can_data_be_shared": "Vous devez avoir 15 ans pour partager vos données."})

        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)  # Retirer password_confirm avant la création
        validated_data['password'] = make_password(validated_data['password'])  # Hash du mot de passe
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