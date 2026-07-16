from django.contrib import admin

from .models import Abikasse, Event, EventParticipation
from .notifications import Notification

admin.site.register(Event)
admin.site.register(Abikasse)
admin.site.register(Notification)
admin.site.register(EventParticipation)
