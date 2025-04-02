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

admin.site.register(Contributor)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'truncated_description', 'issue', 'author', 'created_time')
    list_filter = ('created_time', 'issue__project')
    search_fields = ('description', 'author__username')
    readonly_fields = ('uuid', 'created_time')

    def uuid(self, obj):
        return str(obj.id)
    uuid.short_description = 'UUID'

    def truncated_description(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    truncated_description.short_description = 'Description'