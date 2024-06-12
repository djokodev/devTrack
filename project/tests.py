from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from project.models import Project, Contributor
from user.models import User


class ProjectAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword123', date_of_birth='2000-01-01'
        )
        self.user2 = User.objects.create_user(
            username='otheruser', email='other@example.com', password='password123', date_of_birth='1995-01-01'
        )
        self.client.force_authenticate(user=self.user)
        self.project_data = {
            'name': 'Test Project',
            'description': 'A test project',
            'type': 'back-end',
            'author': self.user.id,
        }

    def test_create_project(self):
        url = reverse('project-create')
        response = self.client.post(url, self.project_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.get().name, 'Test Project')
        self.assertEqual(Contributor.objects.count(), 1)
        self.assertEqual(Contributor.objects.get().user, self.user)
        self.assertEqual(Contributor.objects.get().role, 'Author')

    def test_add_contributor(self):
        project = Project.objects.create(name='Test Project', description='A test project', type='back-end', author=self.user)
        url = reverse('contributor-add')
        contributor_data = {
            'project': project.id,
            'user': self.user2.id,
            'role': 'Contributor'
        }
        response = self.client.post(url, contributor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contributor.objects.count(), 1)

    
    def test_add_contributor_not_author(self):
        project = Project.objects.create(name='Test Project', description='A test project', type='back-end', author=self.user)
        url = reverse('contributor-add')
        self.client.force_authenticate(user=self.user2)
        contributor_data = {
            'project': project.id,
            'user': self.user2.id,
            'role': 'Contributor'
        }
        response = self.client.post(url, contributor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_get_project_detail(self):
        project = Project.objects.create(name='Test Project', description='A test project', type='back-end', author=self.user)
        Contributor.objects.create(project=project, user=self.user, role='Author')
        url = reverse('project-detail', kwargs={'pk': project.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Project') 

    
    def test_update_project(self):
        project = Project.objects.create(name='Test Project', description='A test project', type='back-end', author=self.user)
        Contributor.objects.create(project=project, user=self.user, role='Author')
        url = reverse('project-update', kwargs={'pk': project.id})
        updated_data = {'name': 'Updated Project', 'description': 'Updated description'}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        project.refresh_from_db()
        self.assertEqual(project.name, 'Updated Project')
        self.assertEqual(project.description, 'Updated description')

    
    def test_delete_project(self):
        project = Project.objects.create(name='Test Project', description='A test project', type='back-end', author=self.user)
        Contributor.objects.create(project=project, user=self.user, role='Author')
        url = reverse('project-delete', kwargs={'pk': project.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Project.objects.filter(pk=project.id).exists())
