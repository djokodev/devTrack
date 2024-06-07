from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Project, Contributor

User = get_user_model()

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'type', 'author']
    
    def create(self, validated_data):
        project = Project.objects.create(**validated_data)
        
        Contributor.objects.create(
            project=project,
            user=project.author,
            role='Author'
        )
        
        return project
    
    
class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['project', 'user', 'role', 'date_added']