from django import forms
from .models import Event, EventParticipation

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['created_by', 'created_at']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class EventParticipationForm(forms.ModelForm):
    class Meta:
        model = EventParticipation
        fields = ['attendance_mode']