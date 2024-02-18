from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime


# Custom User Model
class User(AbstractUser):
    """
    Custom User model.

    This model extends the default Django User model to include an email field and
    a preferred mode field.

    The preferred mode field is used to store the user's preferred color scheme for the
    web application. It is used to determine the color scheme of the web application when
    the user is logged in.
    """

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=255)
    preferred_mode = models.CharField(
        choices=[("dark", "Dark Mode"), ("light", "Light Mode")], default="light"
    )


# User stats Model
class UserStats(models.Model):
    """
    Model to store user statistics.

    This model stores the user's total number of sessions, total time spent in sessions,
    current streak, best streak, and last session date.

    The current streak is the number of consecutive days the user has completed a session. The best
    streak is the maximum number of consecutive days the user has completed a session. The last session
    date is the date of the user's last session.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="userstats"
    )
    total_sessions = models.IntegerField(default=0)
    total_time = models.DurationField(default=datetime.timedelta(0))
    current_streak = models.IntegerField(default=0)
    best_streak = models.IntegerField(default=0)
    last_session_date = models.DateField(null=True, default=None)


# User Session Model
class Sessions(models.Model):
    """
    Model to store user sessions.

    This model stores the user's session start time, end time, duration, session type, and streak.

    The duration is the duration of the session. The session type is the type of session (breathing or
    meditation). The streak is the number of consecutive days the user has completed a session.
    """

    username = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField(editable=False)
    session_type = models.CharField(
        choices=[
            ("Breathing Session", "Breathing session"),
            ("Meditation Session", "Meditation session"),
        ]
    )
    streak = models.IntegerField(default=1)

    class Meta:
        indexes = [models.Index(fields=["username", "end_time"])]

    def save(self, *args, **kwargs):
        self.duration = self.end_time - self.start_time
        super(Sessions, self).save(*args, **kwargs)
