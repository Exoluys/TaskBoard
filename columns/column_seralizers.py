from rest_framework import serializers

from tasks.models import Column


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]