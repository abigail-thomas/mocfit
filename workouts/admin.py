from django.contrib import admin
from .models import MuscleGroup, Exercise, Goal, Equipment, MuscleGroupCategory

# Register your models here.
admin.site.register(MuscleGroup)
admin.site.register(Exercise)
admin.site.register(Goal)
admin.site.register(Equipment)
admin.site.register(MuscleGroupCategory)