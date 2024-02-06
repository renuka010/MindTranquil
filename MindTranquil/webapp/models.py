from django.db import models
from django.contrib.auth.models import AbstractUser

#Custom User Model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=255)
    preferred_mode = models.CharField(choices=[('dark', 'Dark Mode'), ('light', 'Light Mode')],
                                      default='light')
    
