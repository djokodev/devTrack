from rest_framework import permissions

class IsContributor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.contributor_set.filter(user=request.user).exists()
