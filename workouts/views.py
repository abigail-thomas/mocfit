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

        # Workout size scaling
        length_map = {
            "short": 4,
            "medium": 6,
            "long": 8,
        }
        target_exercises = length_map.get(selected_length, 6)

        # Sets/Reps templates by goal
        goal_sets_reps = {
            "strength": {"sets": 4, "reps": "4-6"},
            "hypertrophy": {"sets": 3, "reps": "8-12"},
            "endurance": {"sets": 2, "reps": "15-20"},
        }
        default_sr = {"sets": 3, "reps": "10-12"}
        sr = goal_sets_reps.get(selected_goal, default_sr)

        generated = {}

        for muscle_name in selected_muscles:
            try:
                muscle = MuscleGroup.objects.get(name=muscle_name)

                # Base queryset
                exercises = Exercise.objects.filter(primary_muscle=muscle)

                if selected_difficulty:
                    exercises = exercises.filter(difficulty=selected_difficulty)
                if selected_goal:
                    exercises = exercises.filter(goals__name=selected_goal)
                if selected_equipment:
                    exercises = exercises.filter(equipment__name=selected_equipment)

                # Split into compound & isolation
                compounds = list(exercises.filter(mechanics="compound"))
                isolations = list(exercises.filter(mechanics="isolation"))

                chosen = []

                # Always try to pick one compound
                if compounds:
                    chosen.append(random.choice(compounds))

                # Fill with isolations/remaining compounds
                remaining_slots = max(1, target_exercises // len(selected_muscles)) - len(chosen)
                if remaining_slots > 0:
                    pool = isolations if isolations else compounds
                    if pool:
                        chosen.extend(random.sample(pool, min(len(pool), remaining_slots)))

                # Attach sets/reps to each exercise
                generated[muscle.name] = [
                    {
                        "exercise": ex,
                        "sets": sr["sets"],
                        "reps": sr["reps"],
                    }
                    for ex in chosen
                ]

            except MuscleGroup.DoesNotExist:
                generated[muscle_name] = []

        return render(
            request,
            "workouts/workout_results.html",
            {
                "workout": generated,
                "goal": selected_goal,
                "length": selected_length,
            },
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