from django.contrib import admin
from authentication.models import User
from api.models import Project, Contributor, Issue, Comment

class ContributorInline(admin.TabularInline):  # Affiche les contributeurs sous forme de tableau
    model = Contributor
    extra = 1  # Nombre de lignes vides pour ajouter des contributeurs

class ProjectAdmin(admin.ModelAdmin):
    inlines = [ContributorInline]  # Ajoute les contributeurs directement sur la page d'édition d'un projet

admin.site.register(User)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue)
admin.site.register(Comment)
admin.site.register(Contributor)