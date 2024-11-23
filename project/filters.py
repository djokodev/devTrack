import django_filters
from project.models import Project

class ProjectFilter(django_filters.FilterSet):
    class Meta:
        model = Project
        fields = ['name', 'description', 'type', 'author']