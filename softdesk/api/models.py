from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class Project(models.Model):
    TYPE_CHOICES = [
        ('back-end', 'Back-end'),
        ('front-end', 'Front-end'),
        ('iOS', 'iOS'),
        ('Android', 'Android'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='authored_projects', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

class Contributor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='contributions', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='contributors', on_delete=models.CASCADE)
