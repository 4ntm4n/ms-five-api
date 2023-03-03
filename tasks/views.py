from rest_framework import generics
from django.http import request
from .models import Task
from .serializers import TaskSerializer
from rest_api.permissions import NoOwnerAndMemberOrOwner
from .filter_backends import IsGroupMemberFilter
from rest_framework.permissions import IsAuthenticated

class TaskListView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all(
    ).order_by('-created_at')

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, NoOwnerAndMemberOrOwner]
    queryset = Task.objects.all()
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

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
    permission_classes = [IsAuthenticated]
    #filter_backend = [IsGroupMemberFilter]

    def get_queryset(self):
        return Task.objects.filter(owning_group__members=self.request.user.profile)

