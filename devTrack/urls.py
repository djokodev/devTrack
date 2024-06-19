from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers
from user.views import UserViewSet
from project.views import ProjecViewSet, ContributorViewSet, ContributedProjectsByUser
from issue.views import IssueViewSet
from comment.views import CommentViewSet

router = routers.SimpleRouter()

router.register('user', UserViewSet, basename='user')
router.register('project', ProjecViewSet, basename='project')
router.register('contributor', ContributorViewSet, basename='contributor')
router.register('contributed-project-byuser', ContributedProjectsByUser, basename='contributed-project-byuser')
router.register('issue', IssueViewSet, basename='issue')
router.register('comment', CommentViewSet, basename='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls))
]
