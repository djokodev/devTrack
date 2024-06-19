from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from user.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserViewSetTests(APITestCase):
    ...
