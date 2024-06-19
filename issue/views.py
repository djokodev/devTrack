from rest_framework import viewsets, serializers
from .serializers import IssueSerializer
from rest_framework.exceptions import PermissionDenied
from .models import Issue
from project.models import Contributor
from devTrack.permission import IsAuthorPermission, IsContributorPermission
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.viewsets import GenericViewSet


# class CacheListRetrieveMixin(ListModelMixin, RetrieveModelMixin):
#     @method_decorator(cache_page(60 * 20))
#     def list(self, request, *args, **kwargs):
#         return super().list(request, *args, **kwargs)
    
#     @method_decorator(cache_page(60 * 20))
#     def retrieve(self, request, *args, **kwargs):
#         return super().retrieve(request, *args, **kwargs)
    

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthorPermission]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [IsContributorPermission]
        else: 
            permission_classes = [IsContributorPermission]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        assigned_to = serializer.validated_data.get('assigned_to')
        author = self.request.user

        contributors = Contributor.objects.filter(project=project, user=author)
      
        if not contributors.exists():
            raise PermissionDenied("You are not a contributor to this project.")

        if assigned_to and not Contributor.objects.filter(project=project, user=assigned_to).exists():
            raise serializers.ValidationError("Assignee must be a contributor to this project.")

        serializer.save(author=self.request.user)
