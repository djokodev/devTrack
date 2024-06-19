from rest_framework import permissions

class IsAuthorPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsContributorPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'issue') and obj.issue.project.contributor_set.filter(user=request.user).exists():
            return True
        if hasattr(obj, 'project') and obj.project.contributor_set.filter(user=request.user).exists():
            return True
        return False
