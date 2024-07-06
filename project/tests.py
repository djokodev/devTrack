from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from project.models import Project, Contributor
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()

# class ProjectViewSetTests(APITestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.user = User.objects.create_user(username='testuser', password='testpass')
#         cls.token = RefreshToken.for_user(cls.user)

#     def setUp(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
#         self.url = reverse('project-list')

#     def test_create_project(self):
#         data = {
#             'name': 'Test Project',
#             'description': 'A test project',
#             'type': 'back-end',
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Project.objects.count(), 1)
#         self.assertEqual(Project.objects.get().name, 'Test Project')