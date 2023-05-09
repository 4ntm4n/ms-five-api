from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from .models import Task
from groups.models import Group
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django.db.models import Q




class TaskListView(generics.ListAPIView):
    """
    An endpoint for listing all tasks in the app.
    
    the get_queryset method limits this view to only show tasks related to groups that 
    the requsting user is a member of. you need to be authenticated to see any data.

    The filters allow search on:
    * task title
    * task description
    * task owner username
    * name of group the task belongs to

    the fieldset filters allow for quick filtering on:
    * completed tasks
    * tasks in progress
    * task owner username 
    * task owning group name

    additionally if you want to see all relevant tasks that are un initiated
    you can send a request like so: /tasks/?owner=null
    """
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    #filterset to be used for dropdowns for example
    filterset_fields = ['owner__owner__username', 'owning_group__name', 'owning_group__id', 'completed', 'in_progress']
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


class CreateTaskView(generics.CreateAPIView):
    """
    this is a simple view to handle creation of a new task 
    
    Please Note! you will manually have to set the owning group to the group that you 
    wish to add the task to in the GET request. The serializer will prohibit you from setting
    an owner other than the authenticated user or to create a task for a group you are not a
    member of.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
class CreateGroupTaskView(generics.CreateAPIView):
    """
    This view is designed to create a task for a specific group.
    group is set automatically to the group that is specified in the url. 

    Please Note!
    * if the requesting user is not a member of the group, a permission error is raised.
    * The path for this view is specified in the groups app "groups.urls.py"
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_group(self):
        try:
            group_id = self.kwargs['group_id']
            group = Group.objects.get(id=group_id)
        except (KeyError, Group.DoesNotExist):
            raise Http404
        return group

    def perform_create(self, serializer):
        group = self.get_group()
        if not self.request.user.profile in group.members.all():
            raise PermissionDenied("LOL! you need to be a member of the group you create a task for")
        serializer.save(owning_group=group)
        


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    This view handles all actions that you can perfom on an already existing task
    (GET, PUT, PATCH, UPDATE and DELETE) by its id.
    
    It is especially designed to handle update requests setting the created tasks 
    owner from Null to requesting user. when that happens, the serializer is also
    automatically updating the status of in_progress to true. 

    if the the task is later updated to complete: true, the owner is auto set to 
    Null and in_progress is set to false again. 

    Please Note! If you want to re open the task after it has been completed,
    you need to explicitly set "complete" to False and set the a new owner in
    the PUT request. 
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class TaskEventView(generics.ListAPIView):
    """
    an apiview created to list activities happeneing in the groups a user is a member of. 
    
    it returns the same data as the normal listview but without the filters 
    this is kept as a separate endpoint and view in case we need to add functionality 
    to this specific view later

    it orders by "updated_at" primarely so users can see most recent events on top. 
    in case there is two tasks with the same update date the task will use "create_at"
    as a "fallback" to order by that instead. 
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owning_group__members=self.request.user.profile).order_by('-updated_at', 'created_at')

