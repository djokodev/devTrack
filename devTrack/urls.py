from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers
from user.views import UserViewSet
from project.views import ProjectViewSet, ContributorViewSet, ContributedProjectsByUser
from issue.views import IssueViewSet
from comment.views import CommentViewSet
from rest_framework_nested import routers as nested_routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


router = routers.SimpleRouter()

router.register('user', UserViewSet, basename='user')
router.register('project', ProjectViewSet, basename='project')
router.register('contributor', ContributorViewSet, basename='contributor')
router.register('contributed-project-byuser', ContributedProjectsByUser, basename='contributed-project-byuser')
router.register('issue', IssueViewSet, basename='issue')
router.register('comment', CommentViewSet, basename='comment')

projects_router = nested_routers.NestedDefaultRouter(router, r'project', lookup='project')
projects_router.register(r'contributors', ContributorViewSet, basename='project-contributors')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('api/', include(projects_router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
