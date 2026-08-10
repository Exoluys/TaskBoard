from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from tasks.models import Task
from tasks.task_serializers import TaskSerializer


class TaskListCreateApi(ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(column__board__user=self.request.user)

    def perform_create(self, serializer):
        column = serializer.validated_data["column"]

        if column.board.user != self.request.user:
            raise PermissionDenied("You do not own this board")

        serializer.save()


class TaskDetailApi(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(column__board__user=self.request.user)