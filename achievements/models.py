from django.db import models
from django.contrib.auth.models import User

class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    login_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    date_earned = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "achievement")

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"
