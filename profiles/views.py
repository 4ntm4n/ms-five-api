from rest_framework import generics
from .models import Profile
from .serializers import ProfileSerializer

class ProfileListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all(
    ).order_by('-created_at')