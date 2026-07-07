from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

from .models import Project

User = settings.AUTH_USER_MODEL


class NotificationVerbChoices(models.TextChoices):
    ADDED_TO_PROJECT = ("added_to_project", "Added to project")
    REMOVED_FROM_PROJECT = ("removed_from_project", "Removed from project")


class Notification(models.Model):
    # user is the person who received
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )

    verb = models.CharField(max_length=50, choices=NotificationVerbChoices.choices)

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey("content_type", "object_id")

    is_read = models.BooleanField(default=False)  # pyright: ignore[reportArgumentType]
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.verb == NotificationVerbChoices.ADDED_TO_PROJECT and isinstance(
            self.target, Project
        ):
            return f"Du wurdest zu {self.target.title} hinzugefügt"
        elif self.verb == NotificationVerbChoices.REMOVED_FROM_PROJECT and isinstance(
            self.target, Project
        ):
            return f"Du wurdest aus {self.target.title} entfernt"
        else:
            return f"{self.verb} {self.target.__str__()}"

    def get_url(self) -> str:
        if (
            self.verb == NotificationVerbChoices.ADDED_TO_PROJECT
            or self.verb == NotificationVerbChoices.REMOVED_FROM_PROJECT
        ) and isinstance(self.target, Project):
            return reverse("project-detail", kwargs={"project_id": self.target.pk})

        # fallback
        return reverse("abi")

    def open_as_popup(self) -> bool:
        if (
            self.verb == NotificationVerbChoices.ADDED_TO_PROJECT
            or self.verb == NotificationVerbChoices.REMOVED_FROM_PROJECT
        ) and isinstance(self.target, Project):
            return True

        return False


def notify_participants(project: Project, old, new):
    added = new - old
    removed = old - new

    for participant in added:
        # Notify the participant that they have been added to a project
        Notification(
            user=participant,
            verb=NotificationVerbChoices.ADDED_TO_PROJECT,
            target=project,
        ).save()

    for participant in removed:
        # Notify the participant that they have been removed from a project
        Notification(
            user=participant,
            verb=NotificationVerbChoices.REMOVED_FROM_PROJECT,
            target=project,
        ).save()
