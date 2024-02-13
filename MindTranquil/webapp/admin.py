from django.contrib import admin
from .models import User, UserStats, Sessions

admin.site.register(User)
admin.site.register(UserStats)
admin.site.register(Sessions)