
from rest_framework import serializers, status
from .models import Group
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from rest_framework.response import Response


class GroupSerializer(serializers.ModelSerializer):
    group_owner = ProfileSerializer(read_only=True)
    members = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = [
            'id', 'name', 'description', 'group_owner', 'members', 'created_at', 'updated_at',
        ]
    
    def create(self, validated_data):
        group_owner_profile = self.context['request'].user.profile
        validated_data['group_owner'] = group_owner_profile
        group = super().create(validated_data)
        group.members.add(group_owner_profile)
        return group


class GroupMembersSerializer(serializers.ModelSerializer):
    group_owner = serializers.ReadOnlyField(source='group_owner.id')
    members = ProfileSerializer(many=True, read_only=True)
    profile_id = serializers.IntegerField(write_only=True)

    def get_group_owner(self, obj):
        return ProfileSerializer(obj.group_owner).data

    class Meta:
        model = Group
        fields = [
            'id', 'group_owner', 'members', 'profile_id'
        ]

    def add_member(self, group, profile_id):
        try:
            new_member = Profile.objects.get(id=profile_id)
        except Profile.DoesNotExist:
            raise serializers.ValidationError({'profile_id': 'Invalid profile ID.'})

        if group.members.filter(id=profile_id).exists():
            raise serializers.ValidationError({'profile_id': 'User is already a member of the group.'})

        group.members.add(new_member)
    
    def remove_member(self, group, profile_id):
        try:
            member_to_remove = group.members.get(id=profile_id)
        except Profile.DoesNotExist:
            raise serializers.ValidationError({'profile_id': 'User is not a member of the group.'})
        
        # check if the member_to_remve is also group owner, in which case you receive an error.
        if  member_to_remove == group.group_owner:
            raise serializers.ValidationError({'profile_id': 'Uhm.. Group owners can not be removed from group members...'})

        group.members.remove(member_to_remove)

    def update(self, instance, validated_data):
        profile_id = validated_data.get('profile_id')
        
        if profile_id is not None:
            if profile_id in [member.id for member in instance.members.all()]:
                self.remove_member(instance, profile_id)
            else:
                self.add_member(instance, profile_id)

        return super().update(instance, validated_data)
