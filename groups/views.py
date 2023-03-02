from rest_framework import generics
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
    to add add a member to a group, a PUT request should be sent to this view
    with a the key "profile_id" as context data and the profile "pk" as it's value. 
    eg. {"profile_id":<int:pk>}
    """
    permission_classes = []
    serializer_class = GroupMembersSerializer
    queryset = Group.objects.all()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['profile_id'] = self.request.data.get('profile_id')
        return context

        
    