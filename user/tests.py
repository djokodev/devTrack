from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from user.models import User
from datetime import date, timedelta
from user.serializers import UserSerializer

class UserAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'date_of_birth': '2000-01-01'
        }

        self.invalid_user_data_age = {
            'username': 'younguser',
            'email': 'young@example.com',
            'password': 'password123',
            'date_of_birth': date.today() - timedelta(days=15*365)
        }

    def test_user_creation(self):
        url = reverse('register')
        response = self.client.post(url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_user_profile(self):
        user = User.objects.create_user(**self.user_data)
        url = reverse('profile', kwargs={'pk': user.id})
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_date_of_birth_validation_valid(self):
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())

    def test_date_of_birth_validation_invalid(self):
        serializer = UserSerializer(data=self.invalid_user_data_age)
        self.assertFalse(serializer.is_valid())
        self.assertIn('date_of_birth', serializer.errors)

    def test_update_user_profile(self):
        user = User.objects.create_user(**self.user_data)
        url = reverse('profile', kwargs={'pk': user.id})
        updated_data = {'username': 'updateduser', 'email': 'updated@example.com'}
        self.client.force_authenticate(user=user)
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.username, 'updateduser')
        self.assertEqual(user.email, 'updated@example.com')

    def test_delete_user_profile(self):
        user = User.objects.create_user(**self.user_data)
        url = reverse('profile', kwargs={'pk': user.pk})
        self.client.force_authenticate(user=user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=user.pk).exists())
