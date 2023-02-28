from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Group
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
        group_id = kwargs.get('pk')
        try:
            group = Group.objects.get(id=group_id)
            if group.group_owner == request.user.profile:
                return self.update(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except AttributeError:
            return Response(status=status.HTTP_403_FORBIDDEN)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
