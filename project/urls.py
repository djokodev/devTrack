from django.urls import path
from .views import (
    ProjectCreate, 
    ContributorCreate,
    ContributedProjectsByUser, 
    ProjectDetail, 
    ContributorsByProject,
    ProjectUpdate,
    ProjectDelete
)

urlpatterns = [
    path('user-projects-contributed/', ContributedProjectsByUser.as_view(), name='project-list'),
    path('create/', ProjectCreate.as_view(), name='project-create'),
    path('<int:pk>/update/', ProjectUpdate.as_view(), name='project-update'),
    path('<int:pk>/delete/', ProjectDelete.as_view(), name='project-delete'),
    path('contributor/add/', ContributorCreate.as_view(), name='contributor-add'),
    path('<int:pk>/', ProjectDetail.as_view(), name='project-detail'),
    path('<int:project_id>/contributors/', ContributorsByProject.as_view(), name='project-contributors'),

]
