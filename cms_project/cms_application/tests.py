from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import *

class UserTestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            "name": "Mahesh Kumar Suthar",
            "email": "smaheshparmar3026@gmail.com",
            "password": "mahesh123"
        }

    def test_create_user(self):
        url = reverse('user_view')  
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        self.test_create_user()  
        login_data = {
            "email": "smaheshparmar3026@gmail.com",
            "password": "mahesh123"
        }
        url = reverse('user_login')  
        response = self.client.post(url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostTestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            "name": "Mahesh Kumar Suthar",
            "email": "smaheshparmar3026@gmail.com",
            "password": "mahesh123"
        }
        
        self.client.post(reverse('user_view'), self.user_data, format='json')
        login_data = {
            "email": "smaheshparmar3026@gmail.com",
            "password": "mahesh123"
        }
        response = self.client.post(reverse('user_login'), login_data, format='json')
        self.token = response.data['response']['token']

        self.post_data = {
            "title": "My First Post",
            "description": "This is a post description",
            "content": "Post content here",
            "is_private": False
        }

    def test_create_post(self):
        url = reverse('post_view')  
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)  
        response = self.client.post(url, self.post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_posts(self):
        url = reverse('post_view')  
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)





class LikeTestCase(APITestCase):
    def setUp(self):
        
        self.user_data = {
            "name": "Mahesh Kumar Suthar",
            "email": "smaheshparmar3026@gmail.com",
            "password": "mahesh123"
        }
        self.client.post(reverse('user_view'), self.user_data, format='json')
        login_data = {
            "email": "smaheshparmar3026@gmail.com",
            "password": "mahesh123"
        }
        login_response = self.client.post(reverse('user_login'), login_data, format='json')
        self.token = login_response.data['response']['token']

        
        self.post_data = {
            "title": "My First Post",
            "description": "This is a post description",
            "content": "Post content here",
            "is_private": False
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)  
        post_response = self.client.post(reverse('post_view'), self.post_data, format='json')
        self.post_id = post_response.data['response']['post_id']

    def test_like_post(self):
        url = reverse('like_view', args=[self.post_id])  
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)  
        response = self.client.post(url)  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(post_id=self.post_id, user_id__email=self.user_data['email']).exists())

    def test_double_like_post(self):
        
        url = reverse('like_view', args=[self.post_id])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.client.post(url)
        
        
        response = self.client.post(url)  
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  

    def test_unlike_post(self):
        
        url = reverse('like_view', args=[self.post_id])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.client.post(url)

        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Like.objects.filter(post_id=self.post_id, user_id__email=self.user_data['email']).exists())

    def test_unlike_without_liking(self):
        
        url = reverse('like_view', args=[self.post_id])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  
