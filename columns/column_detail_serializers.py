from rest_framework import serializers

from columns.models import Column
from tasks.task_serializers import TaskSerializer


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