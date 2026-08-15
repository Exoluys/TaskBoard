from rest_framework import serializers

from tasks.models import Column
from tasks.task_serializers import TaskSerializer


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class ColumnDetailSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Column
        fields = [
            "id",
            "name",
            "position",
            "created_at",
            "updated_at",
            "tasks",
        ]


class ColumnMoveSerializer(serializers.Serializer):
    position = serializers.IntegerField(min_value=0)