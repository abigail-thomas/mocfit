# - Athentication models and functions
# from django.contrib.auth.models import auth
import json
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from django.core.serializers.json import DjangoJSONEncoder

from workouts.models import SavedWorkout  # Import from your workout app

from .forms import CreateUserForm, LoginForm, ProfileForm, WeightEntryForm


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
            print(form.errors) # debugging
    else:
        form = CreateUserForm() 

    errors = form.errors.as_text() # get the errors in string format
    context = {
        'registerform':form,
        'errors' : errors,
        }
    return render(request, 'accounts/register.html', context=context)




def my_login(request):

    if request.method =='POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next') or request.POST.get('next') or 'dashboard'
            return redirect("dashboard")
            # username = request.POST.get('username')
            # password = request.POST.get('password')

            # user = authenticate(request, username=username, password=password)

            #if user is not None:
            #    auth.login(request, user)
            #    # redirect to dashboard
                #return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password. Please try again")

    else:
        form = AuthenticationForm()

    context = {'loginform': form}
    return render(request, 'accounts/index.html', context=context)


# REMOVED DUPLICATE - Keep only this one dashboard function
@login_required(login_url="my_login")
def dashboard(request):
    saved_workouts = SavedWorkout.objects.filter(user=request.user)
    
    profile = request.user.profile

    # always load user's weight history to display later
    weight_history = profile.weights.all()
        
    weight_history_data = {
        "dates": [entry.date.strftime("%Y-%m-%d") for entry in weight_history[::-1]],
        "weights": [entry.weight for entry in weight_history[::-1]],
    }
    
    context = {
        'saved_workouts': saved_workouts,
        'weight_history': weight_history,
        'weight_history_json': json.dumps(weight_history_data, cls=DjangoJSONEncoder),
    }
    return render(request, 'accounts/dashboard.html', context)


def user_logout(request):

    auth.logout(request)

    return redirect('.')


@login_required(login_url="my_login")
def update_profile(request):
    profile = request.user.profile

    # always load user's weight history to display later
    weight_history = profile.weights.all()

    if request.method == 'POST':

        # Detect which form was submitted
        if 'save_profile' in request.POST:
            profile_form = ProfileForm(request.POST, instance=profile)
            weight_form = WeightEntryForm()  # empty form, not submitted this round

            if profile_form.is_valid():
                profile_form.save()
                return redirect('update_profile')

        elif 'add_weight' in request.POST:
            weight_form = WeightEntryForm(request.POST)
            profile_form = ProfileForm(instance=profile)  # not submitted this round

            if weight_form.is_valid():
                entry = weight_form.save(commit=False)
                entry.profile = profile
                entry.save()
                return redirect('update_profile')

    else:
        # Initial forms on first view load
        profile_form = ProfileForm(instance=profile)
        weight_form = WeightEntryForm()
        
        weight_history_data = {
        "dates": [entry.date.strftime("%Y-%m-%d") for entry in weight_history[::-1]],
        "weights": [entry.weight for entry in weight_history[::-1]],
        }

    return render(request, 'accounts/update_profile.html', {
        'form': profile_form,
        'weight_form': weight_form,
        'weight_history': weight_history,
        'weight_history_json': json.dumps(weight_history_data, cls=DjangoJSONEncoder)
    })
