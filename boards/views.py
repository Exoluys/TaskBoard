from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from boards.board_serializers import BoardSerializer, BoardDetailSerializer
from boards.models import Board


class BoardListCreateApi(ListCreateAPIView):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Board.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BoardDetailApi(RetrieveUpdateDestroyAPIView):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Board.objects.filter(user=self.request.user)


class BoardDetailSpecificApi(RetrieveAPIView):
    serializer_class = BoardDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Board.objects.filter(user=self.request.user)
