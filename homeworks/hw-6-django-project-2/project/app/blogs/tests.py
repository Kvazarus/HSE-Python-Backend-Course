from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Post, Comment


class BlogAPITests(APITestCase):
    def setUp(self):
        self.imposter = User.objects.create_user(
            username='red_imposter',
            password='sussy1337',
            email='red@medbay.sus'
        )
        self.crewmate = User.objects.create_user(
            username='green_crewmate',
            password='sussy1337',
            email='green@admin.sus'
        )

        self.post = Post.objects.create(
            title='Пудж с автонаводкой',
            content='Честно думаю, что у Пуджа точно автонаводящийся хук',
            author=self.imposter
        )

        self.comment = Comment.objects.create(
            post=self.post,
            text='Клевета! Это всё скилл.',
            author=self.imposter
        )

    def test_get_posts_list_anonymous(self):
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_post_detail_anonymous(self):
        response = self.client.get(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Пудж с автонаводкой')

    def test_get_users_list_anonymous(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_comments_list_anonymous(self):
        response = self.client.get('/api/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        data = {'username': 'pink_sus', 'password': 'password123', 'email': 'pink@cafeteria.sus'}
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_authenticated(self):
        self.client.force_authenticate(user=self.crewmate)
        data = {'title': 'alarm!', 'content': 'Джонни, они на деревьях!'}
        response = self.client.post('/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_anonymous(self):
        data = {'title': 'Взлом', 'content': 'меня взломали плаки плаки'}
        response = self.client.post('/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_comment_authenticated(self):
        self.client.force_authenticate(user=self.crewmate)
        data = {'post': self.post.id, 'text': 'Нажми на эту ссылку чтобы увидеть горячих девушек в 3м от вас. (не оборачивайтесь)'}
        response = self.client.post('/api/comments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_anonymous(self):
        data = {'post': self.post.id, 'text': 'shihiteo'}
        response = self.client.post('/api/comments/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_post_author(self):
        self.client.force_authenticate(user=self.imposter)
        response = self.client.delete(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_post_not_author(self):
        self.client.force_authenticate(user=self.crewmate)
        response = self.client.delete(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_anonymous(self):
        response = self.client.delete(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_comment_author(self):
        self.client.force_authenticate(user=self.imposter)
        response = self.client.delete(f'/api/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_comment_not_author(self):
        self.client.force_authenticate(user=self.crewmate)
        response = self.client.delete(f'/api/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_comment_anonymous(self):
        response = self.client.delete(f'/api/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user_self(self):
        self.client.force_authenticate(user=self.imposter)
        response = self.client.delete(f'/api/users/{self.imposter.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_other(self):
        self.client.force_authenticate(user=self.crewmate)
        response = self.client.delete(f'/api/users/{self.imposter.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_anonymous(self):
        response = self.client.delete(f'/api/users/{self.imposter.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_token_success(self):
        data = {
            'username': 'red_imposter',
            'password': 'sussy1337'
        }
        response = self.client.post('/api/token/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_get_token_wrong_password(self):
        data = {
            'username': 'red_imposter',
            'password': 'wrong_password_haha'
        }
        response = self.client.post('/api/token/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)
