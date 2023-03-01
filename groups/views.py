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
    permission_classes = [IsAuthenticated, IsGroupOwner]
    serializer_class = GroupSerializer
    queryset = Group.objects.all()


class GroupMembersView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsGroupOwner]
    serializer_class = GroupMembersSerializer
    queryset = Group.objects.all()

    def put(self, request, *args, **kwargs):
        """
        1. This method takes the profile_id as an argument from the 
        put request sent to this API view (/groups/<int:pk>/members/) as contenxt.
        2. it then tries to add the the member to the view, 
        if it does not already exist in the members list.
        """
        group_id = kwargs.get('pk')
        profile_id = request.data.get('profile_id')

        try:
            group = Group.objects.get(id=group_id)
            
            #check if user already exists in the members list.
            if group.members.filter(id=profile_id).exists():
                return Response({'detail': 'User is already a member of the group'}, status=status.HTTP_400_BAD_REQUEST)
            
            #retreive profile to add to a group
            new_member = Profile.objects.get(id=profile_id)
            
            #add the new member to the group members list
            group.members.add(new_member)

            serializer = self.serializer_class(group)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Group.DoesNotExist:
            return Response({'detail': 'no group found with that id..'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'detail': f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
