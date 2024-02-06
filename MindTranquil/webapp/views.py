from django.shortcuts import render, redirect

from .forms import RegistrationForm, LoginUserForm

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth

#register a new user
def user_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.preferred_mode = 'light'
            user.save()
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
    return render(request, 'webapp/stats.html')

#change dark/light mode view
def change_mode(request):
    if request.user.preferred_mode == 'light':
        request.user.preferred_mode = 'dark'
    else:
        request.user.preferred_mode = 'light'
    request.user.save()
    return redirect('webapp:index')