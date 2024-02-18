from django.apps import AppConfig
from .tasks import update_streak


class WebappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "webapp"

    def ready(self):
        update_streak.delay()
