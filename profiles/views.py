from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from .models import Profile
from .serializers import ProfileSerializer
from rest_api.permissions import IsOwnerOrReadOnly

class ProfileFilterBackend(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        search_query = request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(owner__username__icontains=search_query)
        return queryset


class ProfileListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all(
    ).order_by('-created_at')


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()