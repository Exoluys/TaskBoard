from django.db import transaction
from django.db.models import F
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from columns.column_seralizers import ColumnSerializer, ColumnDetailSerializer, ColumnMoveSerializer
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


class ColumnMoveApi(RetrieveUpdateAPIView):
    serializer_class = ColumnMoveSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        column = self.get_object()
        old_position = column.position

        new_position = serializer.validated_data["position"]

        if column.board.user != request.user:
            raise PermissionDenied("You do not own this board")

        column_count = column.board.columns.count()
        if new_position >= column_count:
            return Response({
                "details": "Invalid position"
            }, status=status.HTTP_400_BAD_REQUEST)

        if new_position == old_position:
            return Response({"details": "No Change"})

        if new_position < old_position:
            Column.objects.filter(
                board=column.board,
                position__gte=new_position,
                position__lt=old_position
            ).update(position=F("position")+1)

        else:
            Column.objects.filter(
                board=column.board,
                position__gt=old_position,
                position__lte=new_position
            ).update(position=F("position")-1)

        column.position = new_position
        column.save()

        return Response({
            "details": "Update Successful",
            "column": ColumnSerializer(column).data
        })

    def get_queryset(self):
        return Column.objects.filter(board__user=self.request.user)