from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class SignupTest(APITestCase):

    def setUp(self):
        self.url = '/signup/'
        self.response = self.client.get(self.url)
    
    def test_if_signup_url_is_working(self):
        response = self.response.status_code
        self.assertEqual(response, status.HTTP_200_OK)