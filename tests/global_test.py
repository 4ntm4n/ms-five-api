from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class AuthTests(APITestCase):

    # endpoints tested in this testcase.
    endpoints = {
        "signup": "/dj-rest-auth/registration/",
        "login": "/dj-rest-auth/login/",
        "logout": "/dj-rest-auth/logout/",
        "user": "/dj-rest-auth/user/",
    }

    # object containig new user data and existing user data
    new_user = {
        "username": "testUser",
        "password1": "Testytester123",
        "password2": "Testytester123",
    }

    def get_existing_user(self):
        return {
            "username": self.new_user["username"],
            "password": self.new_user["password1"],
        }

    def setUp(self):
        """
        sets up a test version of the database,
        creates a url to the registration endpoint, 
        creats user data and then tries to post it to the
        registration endpoind url using json format.  
        """
        url = self.endpoints["signup"]
        data = self.new_user
        self.response = self.client.post(url, data, format='json')

    def test_if_signup_url_is_working(self):
        """
        tests if a user can be created. 204 is a  success since 
        this endpoint will not return a any data, just add a user.
        """
        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)

    def test_if_user_exists_in_database(self):
        """
        here we test if the added user exists by saving the test user to a user variable
        if the user is not created, the user will be None and test will fail
        if user do exist, the user.username will be testUser and the test will pass.
        """
        user = User.objects.filter(username="testUser").first()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testUser')

    def test_if_user_can_login(self):
        """
        1. Test if user can login using dj-rest-auth/login/ expect: Status 200_OK.
        2.Test if user revieces a session token as "key" in response -
        expect: response "key" to not be None.
        """
        url = self.endpoints["login"]
        data = self.get_existing_user()
        response = self.client.post(url, data, format='json')
        self.assertIsNotNone(response.data["key"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_user_can_logout(self):
        """
        1.Test if user is loged in is_auth to be true since last test.
        2.Test if user can reach logout endpoind. expect postrequest 200 OK and sucessmessage
        3.Test again if user is loged in is_auth to be False since now loged out.

        """
        # set the user object and user url
        data = self.get_existing_user()
        user_url = self.endpoints["user"] 

        #save authentication status on current user, anonymos or loged in
        is_auth = response.wsgi_request.user.is_authenticated
        
        #check if user is authenticated from prev test.
        response = self.client.get(user_url, data, format='json')
        self.assertTrue(is_auth)
        
        #check if user can reach logout endpoint and logout.
        url = self.endpoints["logout"]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data["detail"], "Successfully logged out.")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #check if user no longer is authenticated
        response = self.client.get(user_url, data, format='json')
        is_auth = response.wsgi_request.user.is_authenticated
        self.assertFalse(is_auth)
