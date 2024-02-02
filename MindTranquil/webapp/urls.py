from django.urls import path
from . import views

app_name = 'webapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('breathe/', views.breathe, name='breathe'),
]