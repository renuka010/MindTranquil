from __future__ import absolute_import, unicode_literals
from celery import shared_task

from django.utils import timezone

@shared_task
def update_streak():
    from .models import UserStats

    current_date = timezone.now().date()
    user_stats = UserStats.objects.filter(last_session_date__lt = current_date - timezone.timedelta(days=1))
    user_stats.update(current_streak=0)
    print("Streaks updated")