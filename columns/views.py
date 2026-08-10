from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from columns.column_detail_serializers import ColumnDetailSerializer
from columns.column_seralizers import ColumnSerializer
from columns.models import Column


class ColumnListCreateApi(ListCreateAPIView):
    serializer_class = ColumnSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Column.objects.filter(board__user=self.request.user)

    def perform_create(self, serializer):
        board = serializer.validated_data["board"]
        new_position = 0

        if board.user != self.request.user:
            raise PermissionDenied("You do not own this board")

        last_column = board.columns.last()
        if last_column:
            new_position = last_column.position + 1

        serializer.save(position=new_position)


class ColumnDetailApi(RetrieveUpdateDestroyAPIView):
    serializer_class = ColumnSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Column.objects.filter(board__user=self.request.user)


class ColumnDetailSpecificApi(RetrieveAPIView):
    serializer_class = ColumnDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Column.objects.filter(board__user=self.request.user)

