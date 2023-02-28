from profiles.models import Profile
from groups.models import Group
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class TestAuth(APITestCase):

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

    def test_if_logged_in_user_can_logout(self):
        """
        1.Test if user is loged in is_auth to be true since last test.
        2.Test if user can reach logout endpoind. expect postrequest 200 OK and sucessmessage
        3.Test again if user is loged in is_auth to be False since now loged out.

        """
        # set the user object and user url
        data = self.get_existing_user()
        user_url = self.endpoints["user"]

        # check if user is authenticated from prev test.
        response = self.client.get(user_url, data, format='json')
        # save authentication status logedin users are Truthy. expect True.
        is_auth = response.wsgi_request.user.is_authenticated
        self.assertTrue(is_auth)

        # check if user can reach logout endpoint and logout.
        url = self.endpoints["logout"]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data["detail"], "Successfully logged out.")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check if user no longer is authenticated
        response = self.client.get(user_url, data, format='json')
        # save authentication status logedin users are Truthy. expect False.
        is_auth = response.wsgi_request.user.is_authenticated
        self.assertFalse(is_auth)


class TestGroups(APITestCase):
    # endpoints tested
    endpoints = {
        "groups": "/groups/",
    }

    # login / out endpoints
    login = '/dj-rest-auth/login/'
    logout = '/dj-rest-auth/logout/'

    user_cred = {
        "username": "",
        "password": "",
    }

    group_data = {
        "name": "",
        "description": ""
    }

    user = None

    def setUp(self):
        """
        create user in the database
        login user
        """
        User.objects.create(username='TestGroupUser', password="SecretPW123")
        self.user_cred["username"] = User.objects.first().username
        self.user_cred["password"] = User.objects.first().password
        self.user = User.objects.first()

    def test_anonymous_user_can_not_see_groups(self):
        """un-auth users should not be able to see groups"""
        url = self.endpoints["groups"]
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_in_user_can_see_groups_list(self):
        """authorized users should be able to see posts"""
        # login user
        self.client.force_authenticate(user=self.user)

        url = self.endpoints["groups"]
        response = self.client.get(url, format='json')
        # expect to be granted access
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_add_group(self):
    # login user
        self.client.force_authenticate(user=self.user)

        # create post with user
        url = self.endpoints["groups"]
        group_data = {
            "group_owner": self.user.profile.id,
            "name": "test name",
            "description": "test description",
        }
        response = self.client.post(url, group_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check if group was created
        group_id = response.data.get("id")
        self.assertTrue(Group.objects.filter(id=group_id).exists())
        group = Group.objects.get(id=group_id)
        self.assertEqual(group.name, "test name")
        self.assertEqual(group.description, "test description")
        self.assertEqual(group.group_owner.owner.username, self.user.username)
        self.assertEqual(group.members.count(), 0)

