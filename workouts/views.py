from django.shortcuts import render
import random
from .data import workout_list, advanced_workout_list
from .models import Exercise, MuscleGroup

# Create your views here.


def workout_generator_page(request):
    return render(request, "workouts/workout_generator_page.html")

def workout_generator(request, workout_type):
    exercises = workout_list.get(workout_type, [])

    num_to_pick = random.choice([3, 4])
    chosen = random.sample(exercises, k = num_to_pick) if exercises else []

    return render(request, "workouts/workout_results.html", {
        "type": workout_type.capitalize(),
        "exercises": chosen
    })

def advanced_workout_generator(request):
    if request.method == "POST":
        selected_muscles = request.POST.getlist("muscles")
        generated = {}

        for muscle_name in selected_muscles:
            try:
                muscle = MuscleGroup.objects.get(name = muscle_name)
                exercises = Exercise.objects.filter(muscles = muscle)
                generated[muscle.name] = exercises
            except MuscleGroup.DoesNotExist:
                generated[muscle_name] = []
        
        return render(request, "workouts/advanced_workout_results.html", {"workout": generated})

# this function pulled from the workout list in data.py instead of the database in models.py
# def advanced_workout_generator(request):
#     if request.method == "POST":
#         selected_muscles = request.POST.getlist("muscles")
#         generated = {}
#         for muscle in selected_muscles:
#             generated[muscle] = advanced_workout_list.get(muscle, [])
#         return render(request, "workouts/advanced_workout_results.html", {"workout": generated})