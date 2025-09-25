# - Athentication models and functions
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import auth
from django.shortcuts import redirect, render

from .forms import CreateUserForm, LoginForm


def homepage(request):

    #return render(request, "accounts/home.html")
    return render(request, 'accounts/index.html')



def register(request):
    print("register")
    # form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print("worked")
            return redirect("dashboard")
        else:
            print(form.errors)

        
    else:
        form = UserCreationForm()


    context = {'registerform':form}

    

    return render(request, 'accounts/register.html', context=context)




def my_login(request):

    if request.method =='POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
            # username = request.POST.get('username')
            # password = request.POST.get('password')

            # user = authenticate(request, username=username, password=password)

            #if user is not None:
            #    auth.login(request, user)
            #    # redirect to dashboard
                #return redirect("dashboard")
    else:
        form = AuthenticationForm()

    context = {'loginform': form}
    return render(request, 'accounts/index.html', context=context)



@login_required(login_url="my_login")
def dashboard(request):
    return render(request, 'accounts/dashboard.html')



def user_logout(request):

    auth.logout(request)

    return redirect('accounts/my_login')


