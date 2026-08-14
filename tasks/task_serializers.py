from rest_framework import serializers

from columns.models import Column
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = [
            "id",
            "position",
            "created_at",
            "updated_at",
        ]


class TaskMoveSerializer(serializers.Serializer):
    column = serializers.PrimaryKeyRelatedField(queryset=Column.objects.all())
    position = serializers.IntegerField(min_value=0)