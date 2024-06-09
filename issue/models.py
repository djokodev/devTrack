from django.db import models
from project.models import Project
from django.contrib.auth import get_user_model

User = get_user_model()

class Issue(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.CharField(max_length=50, choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')])
    nature = models.CharField(max_length=50, choices=[('BUG', 'Bug'), ('FEATURE', 'Feature'), ('TASK', 'Task')])
    status = models.CharField(max_length=50, choices=[('TODO', 'To Do'), ('IN_PROGRESS', 'In Progress'), ('FINISHED', 'Finished')])
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

