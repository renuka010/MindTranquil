from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

from .models import User

class RegistrationForm(UserCreationForm):
    '''
        Form for user registration.

        This form extends the default Django UserCreationForm.
    '''
    class Meta:
        model = User
        fields = ['username','email','password1','password2'] # fields to display
    username = forms.CharField(widget=TextInput(attrs={'size': '50'}))
    email = forms.EmailField(widget=TextInput(attrs={'size': '50'}))
    password1 = forms.CharField(widget=PasswordInput(attrs={'size': '50'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'size': '50'}))

class LoginUserForm(AuthenticationForm):
    '''
        Form for user login.

        This form extends the default Django AuthenticationForm.
    '''
    class Meta:
        model = User
        fields = ['username', 'password'] # fields to display
    username = forms.CharField(widget=TextInput(attrs={'size': '37'}))
    password = forms.CharField(widget=PasswordInput(attrs={'size': '37'}))