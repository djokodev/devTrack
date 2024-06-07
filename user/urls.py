from django.urls import path, include
from .views import UserCreateView, UserDetailView

urlpatterns = [
   path('register/', UserCreateView.as_view(), name='register'),
   path('profile/<int:pk>/', UserDetailView.as_view(), name='profile'),
]
