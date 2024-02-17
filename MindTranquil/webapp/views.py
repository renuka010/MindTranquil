from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth

from .forms import RegistrationForm, LoginUserForm
from .models import UserStats, Sessions
from .serializers import UserSerializer, SessionsSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from datetime import timedelta
import datetime

#register a new user
def user_registration(request):
    '''
    Handles user registration.

    This function processes POST requests to register a new user. If the request method is POST and the 
    form data is valid, it creates a new user and logs the user in. It also creates a new UserStats object 
    for the user. If the registration is successful, it redirects to the index page.

    If the request method is not POST or the form data is not valid, it renders the registration form.
    '''
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
            messages.error(request, 'There was a problem with your registration.')
    else:
        form = RegistrationForm()
    return render(request, 'webapp/register.html', {'form': form})


#login a user
def user_login(request):
    '''
        Logs in a user based on provided credentials.

        This view function handles the user login process. It accepts a POST request containing 
        the user's username and password. If the provided credentials are valid, the user is 
        logged in, and they are redirected to the home page. If the credentials are invalid or 
        the request method is not POST, the login form is rendered for the user to retry.
    '''
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
    '''
        Logs out a user.

        This view function logs out the current user, clears the session and redirects to the home page.
    '''
    auth.logout(request)
    return redirect('webapp:index')


# homepage
def index(request):
    '''
        Renders the home page.

        This view function renders the home page. If the user is logged in, it passes the user object
    '''
    context = {'user': request.user}
    return render(request, 'webapp/index.html', context=context)


#redirect to breathe
@login_required(login_url='webapp:login')
def breathe(request):
    '''
        Renders the breathe page.
        
        This view function renders the personalized breathing page.
    '''
    return render(request, 'webapp/breathe.html')

#redirect to meditate
@login_required(login_url='webapp:login')
def meditate(request):
    '''
        Renders the meditate page.
        
        This view function renders the personalized meditation page.
    '''
    music_types = {0: 'No Sound', 1: 'Fireplace', 2: 'Rain in Forest', 3: 'Rain', 4: 'River'}
    return render(request, 'webapp/meditate.html', context={'music_types': music_types})

#redirect to stats
@login_required(login_url='webapp:login')
def stats(request):
    '''
        Renders the stats page.
        
        This view function renders the user statistics page.
    '''
    stats = UserStats.objects.get(user=request.user)

    context = {'stats': stats}
    return render(request, 'webapp/stats.html', context=context)

    
#API view for updating mode
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_mode_api(request):
    '''
        Updates the user's preferred mode.
        
        This view function updates the user's preferred mode. It accepts a POST request containing the
        user's preferred mode. If the request method is POST and the data is valid, it updates the user's
        preferred mode and returns a success message. If the request method is not POST or the data is not
        valid, it returns an error message.
    '''
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
    '''
        Updates the user's session statistics.
        
        This view function updates the user's session statistics. It accepts a POST request containing the
        session data. If the request method is POST and the data is valid, it creates a new session and
        updates the user's statistics. It returns a success message. If the request method is not POST or
        the data is not valid, it returns an error message.
    '''
    data = {**request.data, 'username': request.user.id}
    serializer = SessionsSerializer(data=data)
    end_time = datetime.datetime.strptime(request.data.get('end_time'), "%Y-%m-%dT%H:%M:%S.%fZ")
    if serializer.is_valid() and not (end_time.hour == 0 and end_time.minute == 0):
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
    '''
        Returns the user's active days and session data for a given month and year.

        This view function returns the user's active days and session data for a given month and year.
        It accepts a GET request containing the month and year. If the request method is GET and the
        data is valid, it returns the active days and session data. If the request method is not GET or
        the data is not valid, it returns an error message.
    '''
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
    '''
        Renders the breathing session.
        
        This view function renders the breathing session.
    '''
    return render(request, 'webapp/play_music.html', context={'data': request.POST})
    
#redirect to meditation session
@login_required(login_url='webapp:login')
def play_session(request):
    '''
        Renders the meditation session.
        
        This view function renders the meditation session.
    '''
    return render(request, 'webapp/play_session.html', context={'data': request.POST})

