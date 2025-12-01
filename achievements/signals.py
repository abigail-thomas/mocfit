# achievements/signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import UserProfile, Achievement, UserAchievement
from workouts.signals import workout_generated

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

@receiver(workout_generated)
def track_workouts_and_award(sender, user, **kwargs):
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.workouts_generated += 1
    profile.save()

    milestones = {
        1: "First Workout",
        5: "Generated 5 workouts",
        10: "Generated 10 workouts",
        25: "Generated 25 workouts",
    }

    if profile.workouts_generated in milestones:
        achievement_name = milestones[profile.workouts_generated]
        achievement, _ = Achievement.objects.get_or_create(
            name=achievement_name,
            defaults={"description": f"Generated {profile.workouts_generated} workouts"},
        )
        UserAchievement.objects.get_or_create(user=user, achievement=achievement)