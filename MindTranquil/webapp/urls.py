from django.urls import path
from . import views

app_name = 'webapp'

urlpatterns = [
    path('register/', views.user_registration, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    path('', views.index, name='index'),
    path('breathe/', views.breathe, name='breathe'),
    path('meditate/', views.meditate, name='meditate'),
    path('stats/', views.stats, name='stats'),
]