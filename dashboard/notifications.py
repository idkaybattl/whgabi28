from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

from .models import Event

User = settings.AUTH_USER_MODEL


class NotificationVerbChoices(models.TextChoices):
    ADDED_TO_PROJECT = ("added_to_event", "Added to event")
    REMOVED_FROM_PROJECT = ("removed_from_event", "Removed from event")


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
            self.target, Event
        ):
            return f"Du wurdest zu {self.target.title} hinzugefügt"
        elif self.verb == NotificationVerbChoices.REMOVED_FROM_PROJECT and isinstance(
            self.target, Event
        ):
            return f"Du wurdest aus {self.target.title} entfernt"
        else:
            return f"{self.verb} {self.target.__str__()}"

    def get_url(self) -> str:
        if (
            self.verb == NotificationVerbChoices.ADDED_TO_PROJECT
            or self.verb == NotificationVerbChoices.REMOVED_FROM_PROJECT
        ) and isinstance(self.target, Event):
            return reverse("event-detail", kwargs={"event_id": self.target.pk})

        # fallback
        return reverse("main-page")

    def open_as_popup(self) -> bool:
        if (
            self.verb == NotificationVerbChoices.ADDED_TO_PROJECT
            or self.verb == NotificationVerbChoices.REMOVED_FROM_PROJECT
        ) and isinstance(self.target, Event):
            return True

        return False


def notify_participants(event: Event, old, new):
    added = new - old
    removed = old - new

    for participant in added:
        # Notify the participant that they have been added to an event
        Notification(
            user=participant,
            verb=NotificationVerbChoices.ADDED_TO_PROJECT,
            target=event,
        ).save()

    for participant in removed:
        # Notify the participant that they have been removed from an event
        Notification(
            user=participant,
            verb=NotificationVerbChoices.REMOVED_FROM_PROJECT,
            target=event,
        ).save()
