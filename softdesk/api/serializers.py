from rest_framework.serializers import ModelSerializer
 
from authentication.models import User
from api.models import Project
 
class UserSerializer(ModelSerializer):
 
    class Meta:
        model = User
        fields = ['id', 'username']

class ProjectSerializer(ModelSerializer):
 
    class Meta:
        model = Project
        fields = ['id', 'name']