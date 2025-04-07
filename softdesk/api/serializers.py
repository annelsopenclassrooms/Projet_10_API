from rest_framework.serializers import ModelSerializer, ValidationError, CharField
from authentication.models import User
from api.models import Project, Contributor, Issue, Comment
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.utils.timezone import now


class UserSerializer(ModelSerializer):
    password_confirm = CharField(write_only=True)  # Added password confirmation field

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password_confirm', 'date_of_birth', 'can_be_contacted',
                  'can_data_be_shared']
        extra_kwargs = {
            'password': {'write_only': True},  # Hide password field in the API
        }

    def validate(self, data):
        request = self.context.get('request')
        is_creation = request and request.method == 'POST'

        date_of_birth = data.get('date_of_birth')
        can_data_be_shared = data.get('can_data_be_shared', False)
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        if is_creation and not date_of_birth:
            raise ValidationError(
                    {"date_of_birth": "La date de naissance est obligatoire lors de la création du compte."})

        if password and password != password_confirm:
            raise ValidationError({"password_confirm": "Les mots de passe ne correspondent pas."})

        # Check if the user is under 15 years old
        if date_of_birth:  # Check if date_of_birth is provided
            age = (now().date() - date_of_birth).days // 365
            if can_data_be_shared and age < 15:
                raise ValidationError({"can_data_be_shared": "Vous devez avoir 15 ans pour partager vos données."})

        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)  # Remove password_confirm before saving
        validated_data['password'] = make_password(validated_data['password'])  # Password hashing
        return super().create(validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'type', 'author', 'created_time']
        extra_kwargs = {
            'author': {'read_only': True},  # Prevent modification via the API
            'created_time': {'read_only': True},
        }


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project']


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'description', 'project',
            'author', 'assignee', 'priority', 'tag',
            'status', 'created_time'
        ]
        read_only_fields = ['author', 'created_time']

    def validate(self, data):
        user = self.context['request'].user
        project = data.get('project')
        assignee = data.get('assignee')

        # Check that the user is a contributor to the project
        if not Contributor.objects.filter(project=project, user=user).exists():
            raise serializers.ValidationError(
                {"project": "Vous n'êtes pas contributeur de ce projet"}
            )

        # Verify the assignee if provided
        if assignee and not Contributor.objects.filter(project=project, user=assignee).exists():
            raise serializers.ValidationError(
                {"assignee": "L'assigné doit être un contributeur du projet"}
            )

        # Set default status
        if not data.get('status'):
            data['status'] = 'To Do'

        return data


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'description', 'issue', 'author', 'created_time']
        read_only_fields = ['id', 'author', 'created_time']

    def validate(self, data):
        user = self.context['request'].user
        issue = data.get('issue')
        # Check that the user is a contributor to the project
        if not Contributor.objects.filter(project=issue.project, user=user).exists():
            raise serializers.ValidationError(
                {"issue": "Vous n'êtes pas contributeur de ce projet"}
            )
        return data
