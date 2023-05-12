from rest_framework import filters

class IsGroupMemberFilter(filters.BaseFilterBackend):
    """
    checks if the current_user's profile (logged in user's profile)
    is present in the list of members in a group listed in the group list view.
    """
    def filter_queryset(self, request, queryset, view):
        current_user = request.user.profile
        return [group for group in queryset if current_user in group.members.all()]



