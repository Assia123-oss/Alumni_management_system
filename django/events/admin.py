from django.contrib import admin
from .models import Event, EventParticipation

admin.site.register(Event)
admin.site.register(EventParticipation)