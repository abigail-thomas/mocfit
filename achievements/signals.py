# achievements/signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import UserProfile, Achievement, UserAchievement

@receiver(user_logged_in)
def track_logins_and_award(sender, request, user, **kwargs):
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.login_count += 1
    profile.save()

    milestones = {
        1: "First Login",
        3: "Logged in 3 times",
        5: "Logged in 5 times",
        10: "Logged in 10 times"
    }

    if profile.login_count in milestones:
        achievement_name = milestones[profile.login_count]
        achievement, _ = Achievement.objects.get_or_create(
            name=achievement_name,
            defaults={"description": f"Logged in {profile.login_count} times"}
        )
        UserAchievement.objects.get_or_create(user=user, achievement=achievement)