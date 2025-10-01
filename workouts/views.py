from django.shortcuts import render
import random
from .data import workout_list, advanced_workout_list
from .models import Exercise, MuscleGroup, Goal, Equipment, MuscleGroupCategory

# Create your views here.


def workout_generator_page(request):
    categories = MuscleGroupCategory.objects.all()

    goals = Goal.objects.all()
    equipment = Equipment.objects.all()
    muscles = MuscleGroup.objects.all()

    context = {"categories": categories, "goals": goals, "equipment": equipment, "muscles": muscles}
    return render(request, "workouts/workout_generator_page.html", context)

def workout_generator(request):
    if request.method == "POST":
        selected_category = request.POST.get("category")
        try:
            category = MuscleGroupCategory.objects.get(name__iexact=selected_category)
            muscles = category.muscles.all()

            # ✅ filter by primary muscles only
            exercises = Exercise.objects.filter(primary_muscle__in=muscles).distinct()
        except MuscleGroupCategory.DoesNotExist:
            exercises = []

        return render(request, "workouts/workout_results.html", {
            "category": selected_category,
            "exercises": exercises
        })
    else:
        categories = MuscleGroupCategory.objects.all()
        return render(request, "workouts/workout_generator_page.html", {
            "categories": categories
        })


def advanced_workout_generator(request):
    if request.method == "POST":
        selected_muscles = request.POST.getlist("muscles")
        selected_difficulty = request.POST.get("difficulty")
        selected_goal = request.POST.get("goal")
        selected_equipment = request.POST.get("equipment")
        selected_length = request.POST.get("length")

        length_map = {
            "short": 4,
            "medium": 6,
            "long": 8,
        }
        target_exercises = length_map.get(selected_length, 6)

        generated = {}

        for muscle_name in selected_muscles:
            try:
                muscle = MuscleGroup.objects.get(name=muscle_name)

                exercises = Exercise.objects.filter(primary_muscle=muscle)

                if selected_difficulty:
                    exercises = exercises.filter(difficulty=selected_difficulty)
                if selected_goal:
                    exercises = exercises.filter(goals__name=selected_goal)
                if selected_equipment:
                    exercises = exercises.filter(equipment__name=selected_equipment)

                exercises = list(exercises)
                if exercises:
                    num_to_pick = min(len(exercises), max(1, target_exercises // len(selected_muscles)))
                    exercises = random.sample(exercises, num_to_pick)

                generated[muscle.name] = exercises
            except MuscleGroup.DoesNotExist:
                generated[muscle_name] = []

        return render(
            request,
            "workouts/advanced_workout_results.html",
            {"workout": generated, "goal": selected_goal, "length": selected_length}
        )

    else:
        muscles = MuscleGroup.objects.all()
        goals = Goal.objects.all()
        equipment = Equipment.objects.all()
        return render(
            request,
            "workouts/workout_generator_page.html",
            {"muscles": muscles, "goals": goals, "equipment": equipment}
        )
