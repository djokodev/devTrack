from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from project.models import Project, Contributor
from django.contrib.auth import get_user_model

User = get_user_model()

class ProjectViewSetTests(APITestCase):
    ...