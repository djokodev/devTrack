from rest_framework import serializers
from .models import Issue

class IssueSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Issue
        fields = '__all__'
