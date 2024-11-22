from .models import Project, Contributor
from .serializers import (
    ProjectSerializer,
    ContributorSerializer,
    ProjectDetailSerializer,
)
from devTrack.permission import IsAuthorPermission, IsContributorPermission
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthorPermission]

    def get_serializer_class(self):
        if self.action == "retrieve":
            self.serializer_class = ProjectDetailSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        user = self.request.user
        project = serializer.save(author=user)
        if not Contributor.objects.filter(project=project, user=user).exists():
            Contributor.objects.create(
                project=project, user=project.author, role="Author"
            )

    @action(detail=False, methods=['get'])
    def not_issues_projects(self, request):
        """
        Renvoie tous les projets sans issues associés.
        """
        user = request.user

        if not user.is_authenticated:
            return Response(
                {"error": "Vous devez être authentifié pour accéder à cette ressource."},
                status=401,
            )

        not_issues_in_projects = Project.objects.filter(author=user, issues__isnull=True).distinct()
        serializer = self.get_serializer(not_issues_in_projects, many=True)
        return Response(serializer.data)

class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsContributorPermission]

    def get_queryset(self):
        project_pk = self.kwargs["project_pk"]
        return Contributor.objects.filter(project_id=project_pk)

    def perform_create(self, serializer):
        project = serializer.validated_data["project"]
        user = self.request.user
        if project.author != user:
            raise serializers.ValidationError(
                "Only the author of the project can add contributors."
            )
        serializer.save()


class ContributedProjectsByUser(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(contributor__user=user).distinct()
