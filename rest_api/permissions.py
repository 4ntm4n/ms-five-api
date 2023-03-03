from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class IsGroupOwner(permissions.BasePermission):
    """
    custom permission class to prohibit anyone other than a group owner
    to reach  the view. The owner of a group is always a users related profile.
    """
    def has_object_permission(self, request, view, obj):
        return obj.group_owner == request.user.profile

class NoOwnerAndMemberOrOwner(permissions.BasePermission):
    """
    Custom permission class, Gives permission if request.user.profile is 
    member of group.members and task.owner is None. permission is also granted for
    task.owner if a task owner is set.
    """
    def has_object_permission(self, request, view, obj):

        # check if user is not member of the group
        if request.user.profile not in obj.owning_group.members.all():
            return False

        # check if task owner is NOT set to None and task owner is not the reqeusting user.
        if obj.owner is not None and obj.owner != request.user:
            return False

        # check if member of the task's group and the request is get(read), grant access.
        if request.method == 'GET' and request.user.profile in obj.owning_group.members.all():
            return True

        # if logic makes it here, it means that the requesting user IS in fact 
        # the owner of the task OR that the object has no owner and requesting 
        # user is a member of the task's owning group. 
        # And in that case he or she shall be granted priveliges to get put patch 
        # delete anything related to the task :). So we return True....
        return True