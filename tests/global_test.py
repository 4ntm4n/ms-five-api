from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class SignupTest(APITestCase):

    def setUp(self):
        url = '/dj-rest-auth/registration/'
        data = {
            "username": "testUser",
            "password1": "Testytester123",
            "password2": "Testytester123"
        }
        self.response = self.client.post(url, data, format='json')

    def test_if_signup_url_is_working(self):
        """
        tests if a user can be created. 204 == success, 
        since this endpoint will not return a any data, just add a user.
        """
        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)

