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