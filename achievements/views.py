from django.shortcuts import render
from .models import UserAchievement

def my_achievements(request):
    achievements = UserAchievement.objects.filter(user=request.user)
    return render(request, "achievements/my_achievements.html", {"achievements": achievements})
