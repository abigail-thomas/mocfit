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
    muscles = models.ManyToManyField(MuscleGroup, related_name = "exericses")
    mechanics = models.CharField(max_length = 20, choices = MECHANICS_CHOICES, blank = True)
    equipment = models.ManyToManyField(Equipment, blank=True)
    difficulty = models.CharField(max_length = 20, choices = DIFFICULTY_CHOICES, default = "beginner")
    goals = models.ManyToManyField(Goal, blank=True)
    description = models.TextField(blank = True, null = True)
    image_url = models.URLField(blank = True, null = True)

    def __str__(self):
        return f"{self.name} ({self.difficulty})"