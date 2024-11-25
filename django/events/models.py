from django.db import models
from users.models import User
from django.conf import settings

class Event(models.Model):
    ATTENDANCE_CHOICES = [
        ('VIRTUAL', 'Virtual'),
        ('ON_CAMPUS', 'On Campus'),
        ('HYBRID', 'Hybrid')
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    is_virtual = models.BooleanField(default=False)
    event_type = models.CharField(max_length=20, choices=ATTENDANCE_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='event_images/', blank=True)
    max_participants = models.PositiveIntegerField(default=0)
    
    def is_full(self):
        if not self.max_participants:
            return False
        return self.event_participations.count() >= self.max_participants

    def __str__(self):
        return self.title

class EventParticipation(models.Model):
    PARTICIPATION_MODE = [
        ('VIRTUAL', 'Virtual'),
        ('ON_CAMPUS', 'On Campus')
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_participations')
    alumni = models.ForeignKey('alumni.Alumni', on_delete=models.CASCADE, related_name='event_participations')
    attendance_mode = models.CharField(max_length=20, choices=PARTICIPATION_MODE)
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['event', 'alumni']