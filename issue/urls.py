from django.urls import path
from .views import IssueCreate, IssueDetail, IssueDelete, IssueUpdate

urlpatterns = [
    path("create/", IssueCreate.as_view(), name="create-issue"),
    path('<int:pk>/', IssueDetail.as_view(), name='issue-detail'),
    path('<int:pk>/update/', IssueUpdate.as_view(), name='issue-update'),
    path('<int:pk>/delete/', IssueDelete.as_view(), name='issue-delete'),
]
