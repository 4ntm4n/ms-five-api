from rest_framework import serializers
from .models import Group
from profiles.serializers import ProfileSerializer

class GroupSerializer(serializers.ModelSerializer):
    group_owner = ProfileSerializer(read_only=True)

    class Meta:
        model = Group
        fields = [
            'id', 'group_owner', 'name', 'description', 'created_at', 'updated_at',
        ]
    
    def create(self, validated_data):
        validated_data['group_owner'] = self.context['request'].user.profile
        return super().create(validated_data)