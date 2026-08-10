from django.db import models

from columns.models import Column


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    column = models.ForeignKey(
        Column,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    position = models.PositiveIntegerField(default=0, db_index=True)

    title = models.CharField(max_length=225)
    description = models.TextField(blank=True)
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="low"
    )
    due_date = models.DateTimeField(null=True, blank=True)

    # For admin panel
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.column.name}"


    class Meta:
        ordering = ["position"]