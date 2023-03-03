from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Group
from profiles.models import Profile
from .serializers import GroupSerializer, GroupMembersSerializer
from rest_api.permissions import IsGroupOwner
# from rest_framework_simplejwt.authentication import JWTAuthentication


class GroupListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GroupSerializer
    queryset = Group.objects.all(
    ).order_by('-created_at')


class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = []
    serializer_class = GroupSerializer
    queryset = Group.objects.all()


class GroupMembersView(generics.RetrieveUpdateDestroyAPIView):
    """
     To add or remove a member, send a put request with the members profile_id 
     like so: {"profile_id":123}. If no member match the id sent in the request payload, 
     the serializer logic runs the add_member method and tries to add a member to the group.
     If requested id exists, the remove_member method will execute to remove a member. 
    """
    permission_classes = []
    serializer_class = GroupMembersSerializer
    queryset = Group.objects.all()
