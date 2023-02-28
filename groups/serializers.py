from rest_framework import serializers
from .models import Group
from profiles.serializers import ProfileSerializer

class GroupSerializer(serializers.ModelSerializer):
    group_owner = ProfileSerializer(read_only=True)

    class Meta:
        model = Group
        fields = [
            'id', 'name', 'description', 'group_owner', 'members', 'created_at', 'updated_at',
        ]
    
    def create(self, validated_data):
        validated_data['group_owner'] = self.context['request'].user.profile
        return super().create(validated_data)


class GroupMembersSerializer(serializers.ModelSerializer):
    group_owner = ProfileSerializer(read_only=True)
    members = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = [
            'id', 'name', 'group_owner', 'members',
        ]


    def create(self, validated_data):
        validated_data['group_owner'] = self.context['request'].user.profile
        return super().create(validated_data)