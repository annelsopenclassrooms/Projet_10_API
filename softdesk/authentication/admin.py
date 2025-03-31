from django.contrib import admin

# Register your models here.


from authentication.models import User
from api.models import Project, Contributor, Issue, Comment

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Contributor)
admin.site.register(Issue)
admin.site.register(Comment)