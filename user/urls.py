from django.urls import path, include
from .views import UserCreateView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
]
