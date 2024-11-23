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
from drf_spectacular.utils import extend_schema, OpenApiParameter
from project.filters import ProjectFilter



class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthorPermission]
    filterset_class = ProjectFilter

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
    
    @extend_schema(
        operation_id="list_projects_without_issues",
        summary="Liste des projets sans issues",
        description=(
            "Ce endpoint renvoie tous les projets de l'utilisateur connecté "
            "qui n'ont pas d'issues associées."
        ),
        parameters=[
            OpenApiParameter(
                name="Authorization",
                location=OpenApiParameter.HEADER,
                description="Token d'authentification JWT",
                required=True,
                type=str,
            )
        ],
        responses={
            200: ProjectSerializer(many=True),
            401: {"description": "Utilisateur non authentifié"}
        }
    )

    @action(detail=False, methods=['get'], url_path="not-issues-projects")
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
    
    
    @action(detail=False, methods=['get'])
    def active_project(self, request):
        projects = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'],)
    def une_fonction(self, request, pk=None):
        projet = self.get_object()
        return Response({"id": projet.id})
    

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
