from django.urls import path
from .views import IssueCreate

urlpatterns = [
    path("create", IssueCreate.as_view(), name="create-issue"),
]
