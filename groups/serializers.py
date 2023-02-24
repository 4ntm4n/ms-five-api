from rest_framework import serializers
from .models import Group

class GroupSerializer(serializers.ModelSerializer):
    group_owner = serializers.ReadOnlyField()

    class Meta:
        model = Group
        fields = [
            'id','name','description','group_owner','members','created_at','updated_at',
        ]