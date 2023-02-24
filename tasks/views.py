from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer
from rest_api.permissions import IsOwnerOrReadOnly

class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all(
    ).order_by('-created_at')

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Task.objects.all()