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

class IsMember(permissions.BasePermission):
    """
    Custom permission to only allow members of a group associated with the task to view it.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.profile in obj.owning_group.members.all()