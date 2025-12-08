from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class MuscleGroup(models.Model):
    name = models.CharField(max_length = 50, unique = True)

    def __str__(self):
        return self.name

class Goal(models.Model):
    name = models.CharField(max_length = 20, unique = True)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length = 50, unique = True)

    def __str__(self):
        return self.name

class MuscleGroupCategory(models.Model):
    name = models.CharField(max_length = 50, unique = True)
    muscles = models.ManyToManyField("MuscleGroup", related_name = "categories")

    def __str__(self):
        return self.name

class Exercise(models.Model):
    DIFFICULTY_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    MECHANICS_CHOICES = [
        ("isolation", "Isolation"),
        ("compound", "Compound"),
    ]

    name = models.CharField(max_length = 100, unique = True)
    primary_muscle = models.ManyToManyField(MuscleGroup, related_name = "primary_exericses", blank = True)
    secondary_muscles = models.ManyToManyField(MuscleGroup, related_name = "secondary_exercises", blank = True)
    mechanics = models.CharField(max_length = 20, choices = MECHANICS_CHOICES, blank = True)
    equipment = models.ManyToManyField(Equipment, blank=True)
    difficulty = models.CharField(max_length = 20, choices = DIFFICULTY_CHOICES, default = "beginner")
    goals = models.ManyToManyField(Goal, blank=True)
    description = models.TextField(blank = True, null = True)
    image_url = models.URLField(blank = True, null = True)

    def __str__(self):
        return f"{self.name} ({self.difficulty})"
    

# saving wortkouts to profile
class SavedWorkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_workouts')
    title = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    goal = models.CharField(max_length=100, blank=True)
    total_exercises = models.IntegerField(default=0)
    estimated_duration = models.CharField(max_length=50, blank=True)
    workout_data = models.JSONField()  # Stores the complete workout structure
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"