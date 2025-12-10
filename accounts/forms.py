from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput
from .models import Profile, WeightEntry

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
    
# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['height', 'weight', 'birth_date']

class ProfileForm(forms.ModelForm):
    feet = forms.ChoiceField(choices=[(i, i) for i in range(3, 8)])
    inches = forms.ChoiceField(choices=[(i, i) for i in range(0, 12)])

    class Meta:
        model = Profile
        fields = ["feet", "inches", "weight", "birth_date"]  # height is handled manually

    def save(self, commit=True):
        instance = super().save(commit=False)

        feet = int(self.cleaned_data["feet"])
        inches = int(self.cleaned_data["inches"])
        total_inches = feet * 12 + inches

        instance.height = total_inches

        if commit:
            instance.save()
        return instance
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.height:
            total_inches = int(self.instance.height)
            self.initial["feet"] = total_inches // 12
            self.initial["inches"] = total_inches % 12
        
class WeightEntryForm(forms.ModelForm):
    class Meta:
        model = WeightEntry
        fields = ['weight', 'date']