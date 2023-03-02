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
     To add a member, send a put request with the members profile_id like so: {"profile_id":123}.
     To remove a member, send a delete request with the same payload structure {"profile_id":123}
    """
    permission_classes = []
    serializer_class = GroupMembersSerializer
    queryset = Group.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['profile_id'] = self.request.data.get('profile_id')
        return context

    def delete(self, request, *args, **kwargs):
        group = self.get_object()
        profile_id = self.request.data.get('profile_id')
        if profile_id:
            try:
                profile = Profile.objects.get(id=profile_id)
            except Profile.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if profile in group.members.all():
                group.members.remove(profile)
                serializer = self.get_serializer(group)
                return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
