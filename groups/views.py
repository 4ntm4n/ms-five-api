from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Group
from .serializers import GroupSerializer
from rest_api.permissions import IsOwnerOrReadOnly
#from rest_framework_simplejwt.authentication import JWTAuthentication

class GroupListView(generics.ListCreateAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = GroupSerializer
    queryset = Group.objects.all(
    ).order_by('-created_at')


class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()