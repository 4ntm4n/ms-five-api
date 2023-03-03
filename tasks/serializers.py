from rest_framework import serializers
from .models import Task
from profiles.serializers import ProfileSerializer
from groups.serializers import GroupSerializer

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'owning_group', 'owner',
            'in_progress', 'completed', 'created_at', 'updated_at',
        ]