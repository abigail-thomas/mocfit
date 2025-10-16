from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib import auth
from .forms import CreateUserForm, LoginForm, ProfileForm

# - Athentication models and functions
from django.contrib.auth import authenticate, login, logout


def homepage(request):

    #return render(request, "accounts/home.html")
    return render(request, 'accounts/index.html')



def register(request):
    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("my_login")

    context = {'registerform':form}

    return render(request, 'accounts/register.html', context=context)




def my_login(request):

    form = LoginForm()

    if request.method =='POST':
        
        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("dashboard")
            
    context = {'loginform': form}

    return render(request, 'accounts/my_login.html', context=context)



@login_required(login_url="my_login")
def dashboard(request):


    return render(request, 'accounts/dashboard.html')



def user_logout(request):

    auth.logout(request)

    return redirect("")


@login_required
def update_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/update_profile.html', {'form': form})