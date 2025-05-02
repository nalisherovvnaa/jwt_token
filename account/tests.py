from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Post 

# Create your tests here.


class AuthAndCrudTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.auth_headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        self.post_data = {'title': 'Test Post', 'content': 'Test content'}

    def test_jwt_token_auth(self):
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_create_post(self):
        response = self.client.post('/api/posts/', self.post_data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_posts(self):
        Post.objects.create(title='Post 1', content='Content 1', author=self.user)
        response = self.client.get('/api/posts/', **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_post(self):
        post = Post.objects.create(title='Detail View', content='Some content', author=self.user)
        response = self.client.get(f'/api/posts/{post.id}/', **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post(self):
        post = Post.objects.create(title='Old Title', content='Old content', author=self.user)
        updated_data = {'title': 'New Title', 'content': 'Updated content'}
        response = self.client.put(f'/api/posts/{post.id}/', updated_data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_post(self):
        post = Post.objects.create(title='Delete Me', content='To be deleted', author=self.user)
        response = self.client.delete(f'/api/posts/{post.id}/', **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
