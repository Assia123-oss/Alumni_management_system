from users.models import User
from django.db import models
from django.conf import settings

class Alumni(models.Model):
    DEGREE_CHOICES = [
        ('BSC', 'Bachelor of Science'),
        ('BA', 'Bachelor of Arts'),
        ('MSC', 'Master of Science'),
        ('MSC', 'Master of Science'),
        ('PHD', 'Doctor of Philosophy'),
    ]
    
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    graduation_year = models.IntegerField()
    degree = models.CharField(max_length=100, choices=DEGREE_CHOICES)
    current_position = models.CharField(max_length=200, blank=True, null=True)  # Added this field
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=200, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - Class of {self.graduation_year}"

    class Meta:
        verbose_name_plural = "Alumni"
    

