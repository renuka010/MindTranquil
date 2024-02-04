from django.urls import path
from . import views

app_name = 'webapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('breathe/', views.breathe, name='breathe'),
    path('meditate/', views.meditate, name='meditate'),
    path('stats/', views.stats, name='stats'),
]