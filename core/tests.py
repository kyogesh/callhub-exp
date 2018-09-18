from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from .models import create_token

User = get_user_model()


def create_user():
    user = User.objects.create(username='testuser', email='test@user.com', first_name='Test',
                               last_name='User')
    user.set_password('masspass')
    user.save()
    return user


class GetTokenApiTestCase(APITestCase):
    def setUp(self):
        self.user = create_user()

    def test_successful_get_token(self):
        resp = self.client.post(reverse('user:get-token'), {'username': 'testuser',
                                                            'password': 'masspass'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['token'], self.user.auth_token.key)

    def test_unsuccessful_get_token(self):
        resp = self.client.post(reverse('user:get-token'), {'username': 'testuser',
                                                            'password': 'badpass'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('non_field_errors' in resp.data)


class RegisterApiTestCase(APITestCase):

    def test_user_registration(self):
        resp = self.client.post(reverse('core:register'), {'username': 'testuser', 'email': 'test@user.com',
                                                           'first_name': 'Test', 'last_name': 'User',
                                                           'password': 'masspass'})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in resp.data)
        self.assertTrue('username' in resp.data)
