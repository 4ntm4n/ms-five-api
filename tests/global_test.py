from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class SignupTest(APITestCase):

    def setUp(self):
        self.url = 'dj-rest-auth/registration/'
        self.response = self.client.get(self.url)
        print("!!!!!!", self.response.status_code)
    def test_if_signup_url_is_working(self):
        
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)