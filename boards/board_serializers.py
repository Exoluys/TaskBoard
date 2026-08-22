from rest_framework import serializers

from boards.models import Board, BoardMember
from columns.column_seralizers import ColumnDetailSerializer


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = [
            "id",
            "name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


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


class BoardMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardMember
        fields = [
            "id",
            "user",
            "role"
        ]


class BoardMembersSerializer(serializers.Serializer):
    members = BoardMemberSerializer(many=True)