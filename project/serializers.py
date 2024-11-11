from rest_framework import serializers
from .models import Project, Contributor
from issue.models import Issue
from issue.serializers import IssueSerializer
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = "__all__"
        extra_kwargs = {"project": {"required": False}}


class ProjectSerializer(WritableNestedModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    contributors = ContributorSerializer(many=True)
    issues = IssueSerializer(many=True)

    class Meta:
        model = Project
        fields = "__all__"

    def create(self, validated_data):
        contributors_data = validated_data.pop("contributors")
        issues_data = validated_data.pop("issues")
        project = Project.objects.create(**validated_data)

        for contributor_data in contributors_data:
            user = contributor_data.get("user")
            # TODO: utiliser le unique_together
            if not Contributor.objects.filter(project=project, user=user).exists():
                Contributor.objects.create(project=project, **contributor_data)

        for issue_data in issues_data:
            issue_data["author"] = self.context["request"].user
            Issue.objects.create(project=project, **issue_data)

        return project


class ProjectDetailSerializer(serializers.ModelSerializer):

    class EmbededIssueSerializer(serializers.ModelSerializer):
        author = serializers.ReadOnlyField(source="author.username")

        class Meta:
            model = Issue
            fields = ["id", "author", "name"]

    author = serializers.ReadOnlyField(source="author.username")
    contributor_set = ContributorSerializer(many=True, read_only=True)
    issue_set = EmbededIssueSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = "__all__"
