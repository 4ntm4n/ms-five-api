from rest_framework import serializers
from .models import Task
from groups.models import Group
from profiles.serializers import ProfileSerializer
from groups.serializers import GroupSerializer


class TaskSerializer(serializers.ModelSerializer):
    in_progress = serializers.BooleanField()
    completed = serializers.BooleanField()
    owning_group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    group_name = serializers.SerializerMethodField()
    #owner_username = serializers.SerializerMethodField()
    
    def get_group_name(self, obj):
        return obj.owning_group.name if obj.owning_group else None
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'owning_group', 'owner',
            'in_progress', 'completed', 'created_at', 'updated_at', 'group_name'
        ]

    def update(self, instance, validated_data):
        profile = self.context['request'].user.profile
        completed = validated_data.get('completed', instance.completed)
        in_progress = validated_data.get('in_progress', instance.in_progress)
        owner = validated_data.get('owner', instance.owner)
        
        if owner and owner != profile:
            raise serializers.ValidationError("you can not deligate tasks to other users...")

        instance.completed = completed
        if completed:
            instance.in_progress = False
        else:
            instance.in_progress = in_progress
        
        instance.owner = owner
        instance.save()
        return instance
    
    def create(self, validated_data):
        group = validated_data.get('owning_group')
        user = self.context['request'].user
        if not user.is_authenticated or user.profile not in group.members.all():
            raise serializers.ValidationError('You can not create a task for a group you are not a member of. HAHA!')
        task = super().create(validated_data)
        task.owning_group = group
        task.save()
        return task

    