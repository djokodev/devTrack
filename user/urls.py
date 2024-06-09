from django.urls import path, include
from .views import UserCreateView, UserDetailUpdateDestroyView

urlpatterns = [
   path('register/', UserCreateView.as_view(), name='register'),
   path('profile/<int:pk>/', UserDetailUpdateDestroyView.as_view(), name='profile'),
]
