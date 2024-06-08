from rest_framework import generics, serializers
from .models import Project, Contributor
from .serializers import ProjectSerializer, ContributorSerializer
from .permission import IsContributor

class ProjectCreate(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ContributorCreate(generics.CreateAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        user = self.request.user
        if project.author != user:
            raise serializers.ValidationError("Only the author of the project can add contributors.")

        serializer.save()


class ContributedProjectsByUser(generics.ListAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(contributor__user=user).distinct()
    

class ProjectDetail(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsContributor]


class ProjectContributors(generics.ListAPIView):
    serializer_class = ContributorSerializer

    def get_queryset(self):
        project_id = self.kwargs['project_id'] 
        return Contributor.objects.filter(project_id=project_id)
