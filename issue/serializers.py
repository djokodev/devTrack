from rest_framework import serializers
from .models import Issue
from comment.serializers import CommentSerializer

class IssueSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = '__all__'
        extra_kwargs = {'project': {'required': False}}
