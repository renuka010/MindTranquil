from django.urls import path
from . import views

app_name = 'webapp'

urlpatterns = [
    path('register/', views.user_registration, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    path('update_mode_api/', views.update_mode_api, name='update_mode_api'),
    path('update_session_api/', views.update_session_api, name='update_session_api'),
    path('get_active_days_api/', views.get_active_days_api, name='get_active_days_api'),
    
    path('', views.index, name='index'),
    path('breathe/', views.breathe, name='breathe'),
    path('meditate/', views.meditate, name='meditate'),
    path('stats/', views.stats, name='stats'),
    path('play_music/', views.play_music, name='play_music'),
    path('play_session/', views.play_session, name='play_session')
]