from rest_framework import serializers

from boards.models import Board
from columns.column_detail_serializers import ColumnDetailSerializer


class BoardDetailSerializer(serializers.ModelSerializer):
    columns = ColumnDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = [
            "id",
            "name",
            "created_at",
            "updated_at",
            "columns",
        ]
