from rest_framework import permissions

class IsContributor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.contributor_set.filter(user=request.user).exists()
    

class IsIssueContributor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.project.contributor_set.filter(user=request.user).exists()


class IsIssueCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
    

class IsCommentAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user