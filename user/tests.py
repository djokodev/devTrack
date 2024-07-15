from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse_lazy
from user.serializers import UserSerializer
from django.contrib.auth import get_user_model
from datetime import date


User = get_user_model()

class UserViewSetTests(APITestCase):

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'confirm_password': 'testpassword123',
            'date_of_birth': '2000-01-01',
            'can_be_contacted': True,
            'can_data_be_shared': True
        }
        self.url = reverse_lazy('user-list')

    def test_create_user_valid(self):
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
    
    def test_create_user_password_mismatch(self):
        self.user_data['confirm_password'] = 'differentpassword'
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_create_user_underage(self):
    #     self.user_data['date_of_birth'] = date.today().replace(year=date.today().year - 10)
    #     response = self.client.post(self.url, self.user_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn('You must be at least 16 years old to register.', response.data['date_of_birth'])
