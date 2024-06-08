from django.urls import path
from .views import (
    ProjectCreate, 
    ContributorCreate,
    ContributedProjectsByUser, 
    ProjectDetail, 
    ProjectContributors
)

urlpatterns = [
    path('user-projects-contributed/', ContributedProjectsByUser.as_view(), name='project-list'),
    path('create/', ProjectCreate.as_view(), name='project-create'),
    path('contributor/add/', ContributorCreate.as_view(), name='contributor-add'),
    path('<int:pk>/', ProjectDetail.as_view(), name='project-detail'),
    path('<int:project_id>/contributors/', ProjectContributors.as_view(), name='project-contributors'),

]
