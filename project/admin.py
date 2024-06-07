from django.contrib import admin
from .models import Project, Contributor

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'type')

class ContributorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role', 'project', 'date_added')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)