from django.shortcuts import render
from .models import UserAchievement
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/')
def my_achievements(request):
    achievements = UserAchievement.objects.filter(user=request.user)
    return render(request, "achievements/my_achievements.html", {"achievements": achievements})
