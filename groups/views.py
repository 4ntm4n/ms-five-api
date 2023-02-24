from rest_framework import generics
from .models import Group
from .serializers import GroupSerializer
from rest_api.permissions import IsOwnerOrReadOnly

class GroupListView(generics.ListAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.all(
    ).order_by('-created_at')


class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsOwnerOrReadOnly]