from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

# Custom User Model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=255)
    preferred_mode = models.CharField(choices=[('dark', 'Dark Mode'), 
                                               ('light', 'Light Mode')],
                                               default='light')
    
# User stats Model
class UserStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userstats')
    total_sessions = models.IntegerField(default=0)
    total_time = models.DurationField(default=datetime.timedelta(0))
    current_streak = models.IntegerField(default=0)
    best_streak = models.IntegerField(default=0)
    last_session_date = models.DateField(null=True, default=None)

#User Session Model
class Sessions(models.Model):
    
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField(editable=False)
    session_type = models.CharField(choices=
                                    [('Breathing Session', 'Breathing session'), 
                                     ('Meditation Session', 'Meditation session')])
    streak = models.IntegerField(default=1)

    class Meta:
        indexes = [
            models.Index(fields=['username', 'end_time'])
        ]

    def save(self, *args, **kwargs):
        self.duration = self.end_time - self.start_time
        super(Sessions, self).save(*args, **kwargs)