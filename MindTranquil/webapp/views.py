import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse

from .forms import RegistrationForm, LoginUserForm

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer, UserStatsSerializer, SessionsSerializer
from rest_framework.permissions import IsAuthenticated
from .models import UserStats, Sessions

from datetime import timedelta
from django.utils import timezone
from calendar import monthrange

#register a new user
def user_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.preferred_mode = 'light'
            user.save()

            UserStats.objects.create(user=user)

            auth.login(request, user)
            return redirect('webapp:index')
    else:
        form = RegistrationForm()
    return render(request, 'webapp/register.html', {'form': form})

#login a user
def user_login(request):
    if request.method == 'POST':
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('webapp:index')
    else:
        form = LoginUserForm()
    return render(request, 'webapp/login.html', {'form': form})

#logging out
def user_logout(request):
    auth.logout(request)
    return redirect('webapp:index')

# homepage
def index(request):
    context = {'user': request.user}
    return render(request, 'webapp/index.html', context=context)

#redirect to breathe
@login_required(login_url='webapp:login')
def breathe(request):
    return render(request, 'webapp/breathe.html')

#redirect to meditate
@login_required(login_url='webapp:login')
def meditate(request):
    return render(request, 'webapp/meditate.html')

#redirect to stats
@login_required(login_url='webapp:login')
def stats(request):
    stats = UserStats.objects.get(user=request.user)

    context = {'stats': stats}
    return render(request, 'webapp/stats.html', context=context)

    
#API view for updating mode
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_mode_api(request):
    serializer = UserSerializer(instance=request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Preferred mode updated successfully'})
    else:
        return Response({'error': 'Invalid request method'}, status=400)
    
#API view for updating session
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_session_api(request):
    data = {**request.data, 'username': request.user.id}
    serializer = SessionsSerializer(data=data)
    if serializer.is_valid():
        session = serializer.save()

        user_stats = UserStats.objects.get(user=request.user)
        user_stats.total_sessions += 1
        user_stats.total_time += session.duration
        current_date = session.end_time.date()
        if ((not user_stats.last_session_date) or (current_date - user_stats.last_session_date > timedelta(days=1))):
            user_stats.current_streak = 1
        else:
            user_stats.current_streak += 1
        user_stats.best_streak = max(user_stats.best_streak, user_stats.current_streak)
        user_stats.last_session_date = current_date
        user_stats.save()

        return Response({'message': 'Session updated successfully'})
    else:
        return Response({'error': 'Invalid request method'}, status=400)


#API view for getting days active
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_active_days_api(request):
    month = (datetime.datetime.strptime(request.GET.get('month'), '%m')).month
    year = (datetime.datetime.strptime(request.GET.get('year'), '%Y')).year

    sessions = Sessions.objects.filter(username=request.user,
                                       end_time__year=year,
                                       end_time__month=month)
    
    active_days = sessions.values_list('end_time__day', flat=True)

    # Serialize the sessions
    sessions_serializer = SessionsSerializer(sessions, many=True)
    
    data = {
        'active_days': list(active_days),
        'sessions': sessions_serializer.data
    }

    return Response(data)

#redirect to music playing mode
@login_required(login_url='webapp:login')
def play_music(request):
    return render(request, 'webapp/play_music.html', context={'data': request.POST})
    
#redirect to meditation session
@login_required(login_url='webapp:login')
def play_session(request):
    return render(request, 'webapp/play_session.html', context={'data': request.POST})