from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Project(models.Model):
    BACK_END = "back-end"
    FRONT_END = "front-end"
    IOS = "iOS"
    ANDROID = "Android"

    PROJECT_TYPE_CHOICES = [
        (BACK_END, "Back-end"),
        (FRONT_END, "Front-end"),
        (IOS, "iOS"),
        (ANDROID, "Android"),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    type = models.CharField(max_length=10, choices=PROJECT_TYPE_CHOICES)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Contributor(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="contributors"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, default="Contributeur")
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ("project", "user")

    def __str__(self):
        return f"{self.user}"
