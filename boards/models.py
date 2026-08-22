from django.db import models

from backend import settings


class Board(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="boards"
    )
    name = models.CharField(max_length=225)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BoardMember(models.Model):
    ROLE_CHOICES = [
        ("editor", "Editor"),
        ("viewer", "Viewer")
    ]

    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name="members"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="viewer"
    )


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["board", "user"],
                name="unique_board_member"
            )
        ]
