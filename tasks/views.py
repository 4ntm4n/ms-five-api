from rest_framework import generics, request
from django_filters.rest_framework import DjangoFilterBackend
from django.http import request
from .models import Task
from groups.models import Group
from .serializers import TaskSerializer
from rest_api.permissions import NoOwnerAndMemberOrOwner
from .filter_backends import IsGroupMemberFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django.db.models import Q


class TaskListView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    #filterset to be used for dropdowns for example
    filterset_fields = ['owner__owner__username', 'owning_group__name', 'completed', 'in_progress']
    search_fields = ['title', 'description', 'owner__owner__username', 'owning_group__name']
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Get the user's profile
        profile = self.request.user.profile

        # Get all the groups where the profile is a member
        groups = Group.objects.filter(members__id=profile.id)

        # Get all the tasks that belong to those groups
        relevant_tasks = Task.objects.filter(owning_group__in=groups)

        return relevant_tasks

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, ]
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

