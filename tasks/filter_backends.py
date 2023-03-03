from rest_framework import filters
from groups.models import Group

class IsGroupMemberFilter(filters.BaseFilterBackend):
    """
    returns a list of all tasks coming from groups that the current user profile is a member of.
    """
    def filter_queryset(self, request, queryset, view):
        # get current user
        current_user = request.user.profile
        # create a list of group ids in which the user is a member
        
        """ 
        returns the group id for each group inside groups.objects.all()-list
        but only if the current users profile is in the members list of that group
        """
        group_ids = [group.id for group in Group.objects.all() if current_user in group.members.all()]
        
        """
        finally return the queryset after filtering out the tasks that has a parent or 
        "owning_group" with an id that matches one of the ids found in group_ids above
        """
        return queryset.filter(owning_group_id__in=group_ids)