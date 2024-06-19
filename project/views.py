from .models import Project, Contributor
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from .serializers import ProjectSerializer, ContributorSerializer
from devTrack.permission import IsAuthorPermission, IsContributorPermission
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import viewsets, serializers
from rest_framework.viewsets import GenericViewSet


# class CacheListRetrieveMixin(ListModelMixin, RetrieveModelMixin):
#     @method_decorator(cache_page(60 * 20))
#     def list(self, request, *args, **kwargs):
#         return super().list(request, *args, **kwargs)
    
#     @method_decorator(cache_page(60 * 20))
#     def retrieve(self, request, *args, **kwargs):
#         return super().retrieve(request, *args, **kwargs)
    

class ProjecViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthorPermission]

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(
            project=project,
            user=project.author,
            role='Author'
        )


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsContributorPermission]


    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        user = self.request.user
        if project.author != user:
            raise serializers.ValidationError("Only the author of the project can add contributors.")

        serializer.save()


class ContributedProjectsByUser(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(contributor__user=user).distinct()