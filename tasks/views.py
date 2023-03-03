from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer
from rest_api.permissions import IsOwnerOrReadOnly
from .filter_backends import IsGroupMemberFilter

class TaskListView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all(
    ).order_by('-created_at')

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = []
    queryset = Task.objects.all()

class CreateTaskView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = []
    queryset = Task.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class TaskEventView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = []
    filter_backend = [IsGroupMemberFilter]
    queryset = Task.objects.all()

