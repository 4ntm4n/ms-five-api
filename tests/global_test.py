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

from django.forms import model_to_dict

class TestGroups(APITestCase):
    # endpoints tested
    endpoints = {
        "groups": "/groups/",
    }

    # login / out endpoints
    login = '/dj-rest-auth/login/'
    logout = '/dj-rest-auth/logout/'

    #for login
    user_cred = {
        "username": "",
        "password": "",
    }

    
    user = None
    group = None
    profile = None

    extra_user = None

    def setUp(self):
        """
        create users in the database
        """
        # primary user and group used for carry out tests
        user = User.objects.create(username='TestGroupUser', password="SecretPW123")
        group = Group.objects.create(
            group_owner=user.profile, name="test group", description="test description")
        
        self.user = user
        self.group = group
        self.profile = user.profile
        self.user_cred["username"] = User.objects.first().username
        self.user_cred["password"] = User.objects.first().password
        self.user = User.objects.first()
        
        self.extra_user = User.objects.create(username="ExtraUser", password="somePassword123")



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
        data = {
            "name": self.group.name,
            "description": self.group.description,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check if group was created
        group_id = response.data.get("id")
        self.assertTrue(Group.objects.filter(id=group_id).exists())
        group = Group.objects.get(id=group_id)
        self.assertEqual(group.name, "test group")
        self.assertEqual(group.description, "test description")
        self.assertEqual(group.group_owner.owner.username, self.user.username)
        self.assertEqual(group.members.count(), 1)

    def test_GroupDetailView(self):
        """
        test if groupDetail page is reachable. 
        """
        url = f"/groups/{self.group.id}/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_GroupMembersView(self):
        """
        test if member profile can be added to a group using the GroupMemberView.
        """
        # test if groupmembersview is reachable.
        url = f"/groups/{self.group.id}/members/"
        get_response = self.client.get(url, format="json")
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        
        
        #create user to add to the group
        extra_user = self.extra_user

        #try to add member, check for OK response
        data = {
            "profile_id": extra_user.profile.id
        }
        add_response = self.client.put(url, data, format="json")
        self.assertEqual(add_response.status_code, status.HTTP_200_OK)

        #convert group model to a dictionary and check for ExtraUsers's profile in members.
        #if true, extra user is successfully added to the group
        group_dict = model_to_dict(self.group)
        self.assertTrue(extra_user.profile in group_dict["members"])

        #test if user can be removed with a delete request.
        """ del_response = self.client.delete(url, data, format="json")
        self.assertFalse(extra_user.profile in group_dict["members"])
        self.assertEqual(del_response.status_code, status.HTTP_200_OK) """
        