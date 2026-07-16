from .models import EventParticipation
from .notifications import notify_participants


def update_participants(event, selected_users):
    # Remove old participants
    EventParticipation.objects.filter(event=event).exclude(  # pyright: ignore[reportAttributeAccessIssue]
        user__in=selected_users
    ).delete()

    # Add new participants
    existing = set(event.participants.values_list("id", flat=True))
    for user in selected_users:
        if user.id not in existing:
            EventParticipation.objects.create(  # pyright: ignore[reportAttributeAccessIssue]
                event=event,
                user=user,
            )


def save_event(form, user):
    if form.instance.pk:
        old = set(form.instance.participants.all())
    else:
        old = set()

    event = form.save(commit=False)
    event.creator = user
    event.save()

    update_participants(event, form.cleaned_data["participants"])

    new = set(event.participants.all())

    notify_participants(event, old, new)

    return event
