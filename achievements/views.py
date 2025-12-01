from django.shortcuts import render
from .models import UserAchievement
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/')
def my_achievements(request):
    user_achievements = UserAchievement.objects.filter(user=request.user)

    # Separate by achievement name (you can adjust these filters as needed)
    login_achievements = user_achievements.filter(achievement__name__icontains="log")
    workout_achievements = user_achievements.filter(achievement__name__icontains="workout")

    context = {
        "login_achievements": login_achievements,
        "workout_achievements": workout_achievements,
    }

    return render(request, "achievements/my_achievements.html", context)