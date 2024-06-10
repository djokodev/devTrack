from django.urls import path
from .views import CommentCreate, commentDetailUpdateDestroy

urlpatterns = [
    path("create/", CommentCreate.as_view(), name="create-comment"),
    path("<uuid:pk>/", commentDetailUpdateDestroy.as_view(), name="comment-detail-update-delete")
]
