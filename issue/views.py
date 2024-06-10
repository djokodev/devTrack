from rest_framework import generics, serializers
from .serializers import IssueSerializer
from rest_framework.exceptions import PermissionDenied
from .models import Issue
from project.models import Contributor
from devTrack.permission import IsIssueCreator, IsIssueContributor
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

class IssueCreate(generics.CreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        assigned_to = serializer.validated_data.get('assigned_to')
        author = self.request.user

        print("Project:", project)
        print("Author:", author)

        contributors = Contributor.objects.filter(project=project, user=author)
        print("Contributors:", contributors)
      
        if not contributors.exists():
            raise PermissionDenied("You are not a contributor to this project.")

        if assigned_to and not Contributor.objects.filter(project=project, user=assigned_to).exists():
            raise serializers.ValidationError("Assignee must be a contributor to this project.")

        serializer.save(author=self.request.user)


class IssueDetail(generics.RetrieveAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsIssueContributor]
    
    @method_decorator(cache_page(60 * 20)) 
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class IssueUpdate(generics.UpdateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsIssueCreator]

class IssueDelete(generics.DestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsIssueCreator]