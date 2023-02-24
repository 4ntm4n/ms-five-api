from rest_framework import serializers
from .models import Group
from profiles.serializers import ProfileSerializer

class GroupSerializer(serializers.ModelSerializer):
    #add username of group owner
    members = ProfileSerializer(many=True)

    class Meta:
        model = Group
        fields = [
            'id','group_owner','name','description','members','created_at','updated_at',
        ]