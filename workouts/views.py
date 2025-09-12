from django.shortcuts import render
import random
from .data import workout_list

# Create your views here.


def home(request):
    return render(request, "workouts/home.html")

def generate(request, workout_type):
    exercises = workout_list.get(workout_type, [])

    num_to_pick = random.choice([3, 4])
    chosen = random.sample(exercises, k = num_to_pick) if exercises else []

    return render(request, "workouts/result.html", {
        "type": workout_type.capitalize(),
        "exercises": chosen
    })