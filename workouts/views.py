from django.shortcuts import render
import random
from .data import workout_list

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