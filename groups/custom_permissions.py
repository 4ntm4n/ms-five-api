from rest_framework import permissions

class IsGroupMember(permissions.BasePermission):   
    """
    Checks if the current_user's profile (logged in user's profile)
    is present in the list of members in a group.
    """
    def has_object_permission(self, request, view, obj):
        # obj here is a Group instance
        return request.user.profile in obj.members.all()