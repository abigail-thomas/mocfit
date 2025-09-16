from django.db import models

# Create your models here.
class MuscleGroup(models.Model):
    name = models.CharField(max_length = 50, unique = True)

    def __str__(self):
        return self.name

class Exercise(models.Model):
    DIFFICULTY_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    name = models.CharField(max_length = 100, unique = True)
    muscles = models.ManyToManyField(MuscleGroup, related_name = "exercises")
    equipment = models.CharField(max_length = 100, blank = True, null = True)
    difficulty = models.CharField(max_length = 20, choices = DIFFICULTY_CHOICES, default = "beginner")
    description = models.TextField(blank = True, null = True)
    image_url = models.URLField(blank = True, null = True)

    def __str__(self):
        return f"{self.name} ({self.difficulty})"