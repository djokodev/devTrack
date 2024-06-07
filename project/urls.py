from django.urls import path
from .views import ProjectCreateView, ContributorCreateView, UserProjectsContributedListView, ProjectDetailView, ProjectContributorsListView

urlpatterns = [
    path('user-projects-contributed/', UserProjectsContributedListView.as_view(), name='project-list'),
    path('create/', ProjectCreateView.as_view(), name='project-create'),
    path('contributor/add/', ContributorCreateView.as_view(), name='contributor-add'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('<int:project_id>/contributors/', ProjectContributorsListView.as_view(), name='project-contributors'),

]
