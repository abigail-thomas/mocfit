from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True, verbose_name="Birth Date (YYYY-MM-DD)")

    def __str__(self):
        return self.user.username
    
class WeightEntry(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="weights")
    weight = models.FloatField()
    date = models.DateField(null=True, blank=True, verbose_name="Date (YYYY-MM-DD)")  # user can choose the date manually

    class Meta:
        ordering = ['-date']  # newest first

    def __str__(self):
        return f"{self.weight} lbs on {self.date}"