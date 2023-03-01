
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
        validated_data['group_owner'] = self.context['request'].user.profile
        return super().create(validated_data)


class GroupMembersSerializer(serializers.ModelSerializer):
    group_owner = serializers.ReadOnlyField(source='group_owner.id')
    members = ProfileSerializer(many=True, read_only=True)

    def get_group_owner(self, obj):
        return ProfileSerializer(obj.group_owner).data

    class Meta:
        model = Group
        fields = [
            'id', 'group_owner', 'members',
        ]


    def update(self, instance, validated_data):
        profile_id = self.context.get('profile_id')
        if not profile_id:
            raise serializers.ValidationError({'profile_id': 'This field is required.'})

        try:
            new_member = Profile.objects.get(id=profile_id)
        except Profile.DoesNotExist:
            raise serializers.ValidationError({'profile_id': 'Invalid profile ID.'})

        if instance.members.filter(id=profile_id).exists():
            raise serializers.ValidationError({'profile_id': 'User is already a member of the group.'})

        instance.members.add(new_member)

        return instance