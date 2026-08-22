from django.db import transaction, IntegrityError
from rest_framework import serializers, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from boards.board_serializers import BoardSerializer, BoardDetailSerializer, BoardMembersSerializer, \
    BoardMemberSerializer
from boards.models import Board, BoardMember


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


class BoardMemberApi(ListCreateAPIView):
    serializer_class = BoardMembersSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def perform_create(self, serializer):
        members = serializer.validated_data["members"]
        board = Board.objects.get(id=self.kwargs["board"])

        if board.user != self.request.user:
            raise PermissionDenied("You do not own this board")

        seen = set()
        members_to_create = []
        for member in members:
            user = member["user"]

            if user.id in seen:
                raise serializers.ValidationError("User already added")
            seen.add(user.id)

            members_to_create.append(
                BoardMember(
                    board=board,
                    user=user,
                    role=member["role"]
                )
            )

        try:
            BoardMember.objects.bulk_create(members_to_create)
        except IntegrityError:
            raise serializers.ValidationError("One or more users are already members of this board")

    @transaction.atomic
    def patch(self, req, *args, **kwargs):
        serializer = self.get_serializer(data=req.data)
        serializer.is_valid(raise_exception=True)

        board = Board.objects.get(id=self.kwargs["board"])
        if board.user != req.user:
            raise PermissionDenied("You do not own this board")

        new_members = serializer.validated_data["members"]
        user_ids = [member["user"].id for member in new_members]

        members = BoardMember.objects.filter(board=board, user__in=user_ids)
        board_members = {
            member.user.id: member
            for member in members
        }

        members_to_update = []
        for new_member in new_members:
            existing_member = board_members.get(new_member["user"].id)

            if existing_member is None:
                raise serializers.ValidationError("User is not a member of this board")

            existing_member.role = new_member["role"]
            members_to_update.append(existing_member)

        BoardMember.objects.bulk_update(members_to_update, ["role"])

        return Response({"details": "Update Successful"})

    @transaction.atomic
    def delete(self, req, *args, **kwargs):
        serializer = self.get_serializer(data=req.data)
        serializer.is_valid(raise_exception=True)

        board = Board.objects.get(id=self.kwargs["board"])
        if board.user != req.user:
            raise PermissionDenied("You do not own this board")

        new_members = serializer.validated_data["members"]
        user_ids = [member["user"].id for member in new_members]

        BoardMember.objects.filter(
            board=board,
            user__in=user_ids
        ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return BoardMember.objects.filter(board=self.kwargs["board"])

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BoardMemberSerializer

        return BoardMembersSerializer

class BoardMemberDetailApi(RetrieveUpdateDestroyAPIView):
    serializer_class = BoardMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BoardMember.objects.filter(board=self.kwargs["board"])
