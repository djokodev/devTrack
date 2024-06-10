from rest_framework import generics, serializers
from .models import Project, Contributor
from .serializers import ProjectSerializer, ContributorSerializer
from devTrack.permission import IsContributor, IsProjectAuthor
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


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
    
    @method_decorator(cache_page(60 * 20))  
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    

class ProjectDetail(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsContributor]

    @method_decorator(cache_page(60 * 20)) 
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ContributorsByProject(generics.ListAPIView):
    serializer_class = ContributorSerializer

    def get_queryset(self):
        project_id = self.kwargs['project_id'] 
        return Contributor.objects.filter(project_id=project_id)
    
    @method_decorator(cache_page(60 * 20)) 
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    

class ProjectUpdate(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectAuthor]


class ProjectDelete(generics.DestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectAuthor]
