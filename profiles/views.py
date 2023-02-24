from rest_framework import generics
from .models import Profile
from .serializers import ProfileSerializer
from rest_api.permissions import IsOwnerOrReadOnly

class ProfileListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all(
    ).order_by('-created_at')


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()