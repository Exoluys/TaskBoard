from django.db import transaction
from django.db.models import F
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tasks.models import Task
from tasks.task_serializers import TaskSerializer, TaskMoveSerializer


class TaskListCreateApi(ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(column__board__user=self.request.user)

    def perform_create(self, serializer):
        column = serializer.validated_data["column"]
        new_position = 0

        if column.board.user != self.request.user:
            raise PermissionDenied("You do not own this board")

        last_task = column.tasks.last()
        if last_task:
            new_position = last_task.position + 1

        serializer.save(position=new_position)


class TaskDetailApi(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(column__board__user=self.request.user)

class TaskMoveApi(RetrieveUpdateAPIView):
    serializer_class = TaskMoveSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = self.get_object()
        old_column = task.column
        old_position = task.position

        new_column = serializer.validated_data["column"]
        new_position = serializer.validated_data["position"]

        if new_column.board.user != request.user:
            raise PermissionDenied("You do not own this board")

        task_count = Task.objects.filter(column=new_column).count()
        if new_column != old_column:
            task_count += 1

        if new_position >= task_count:
            return Response({
                "details": "Invalid position"
            },status=status.HTTP_400_BAD_REQUEST)

        if new_column == old_column and new_position == old_position:
            return Response({"details": "No change"})

        if new_column == old_column:
            if new_position < old_position:
                Task.objects.filter(
                    column=new_column,
                    position__gte=new_position,
                    position__lt=old_position
                ).update(position=F("position")+1)

            else:
                Task.objects.filter(
                    column=new_column,
                    position__gt=old_position,
                    position__lte=new_position
                ).update(position=F("position")-1)

        if new_column != old_column:
            Task.objects.filter(
                column=old_column,
                position__gt=old_position,
            ).update(position=F("position")-1)

            Task.objects.filter(
                column=new_column,
                position__gte=new_position,
            ).update(position=F("position")+1)

        task.column = new_column
        task.position = new_position
        task.save()

        return Response({
            "details": "Update Successful",
            "task": TaskSerializer(task).data
        })

    def get_queryset(self):
        return Task.objects.filter(column__board__user=self.request.user)