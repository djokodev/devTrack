from rest_framework import generics
from .models import Comment
from .serializers import CommentSerializer
from project.models import Contributor
from rest_framework.exceptions import PermissionDenied
from devTrack.permission import IsCommentAuthor, CommentContributor
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class CommentCreate(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        issue = serializer.validated_data['issue']
        project = issue.project
        if not Contributor.objects.filter(project=project, user=self.request.user).exists():
            raise PermissionDenied("You are not a contributor to this project.")
        serializer.save(author=self.request.user)


class commentDetail(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [CommentContributor]

    @method_decorator(cache_page(60 * 20)) 
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class commentUpdate(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentAuthor]


class commentDelete(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentAuthor]

