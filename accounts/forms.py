from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput
from .models import Profile

# - Create/Register user (Model Form)

class CreateUserForm(UserCreationForm):
    
    class Meta:

        model = User
        ## can add firstname lastname
        fields = ['username', 'email', 'password1', 'password2']


# - Authenticate a user (model form)


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'login-input',
            'placeholder': 'Enter username'
        }))


    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'login-input',
            'placeholder': 'Enter password',
            'id': 'id_password'
        }))
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['height', 'weight', 'birth_date']
	