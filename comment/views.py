from rest_framework import viewsets
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.exceptions import PermissionDenied
from devTrack.permission import IsContributorPermission, IsAuthorPermission
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission]
        elif self.action in ['retrieve', 'list']:
            self.permission_classes = [IsContributorPermission]
        else:
            self.permission_classes = [IsContributorPermission]
        return super().get_permissions()

    def perform_create(self, serializer):
        issue = serializer.validated_data['issue']
        project = issue.project
        if not project.contributor_set.filter(user=self.request.user).exists():
            raise PermissionDenied("You are not a contributor to this project.")
        serializer.save(author=self.request.user)
