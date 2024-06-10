from django.urls import path
from .views import CommentCreate, commentDetail, commentUpdate, commentDelete

urlpatterns = [
    path("create/", CommentCreate.as_view(), name="create-comment"),
    path("<uuid:pk>/", commentDetail.as_view(), name="comment-detail"),
    path("<uuid:pk>/update/", commentUpdate.as_view(), name="comment-update"),
    path("<uuid:pk>/delete/", commentDelete.as_view(), name="comment-delete")
]
