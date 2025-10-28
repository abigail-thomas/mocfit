from django.shortcuts import render
import random
from collections import defaultdict
from django.db.models import Q, Count
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
            "exercises": exercises,
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

        # Enhanced workout size scaling
        length_map = {
            "short": {"total_exercises": 5, "exercises_per_muscle": 2},
            "medium": {"total_exercises": 8, "exercises_per_muscle": 3},
            "long": {"total_exercises": 12, "exercises_per_muscle": 4},
        }
        workout_params = length_map.get(selected_length, length_map["medium"])

        # Goal-based parameters (sets, reps, rest)
        goal_parameters = {
            "strength": {"sets": 4, "reps": "4-6", "rest": "3-5 min"},
            "hypertrophy": {"sets": 3, "reps": "8-12", "rest": "1-2 min"},
            "endurance": {"sets": 2, "reps": "15-20", "rest": "30-60 sec"},
        }
        params = goal_parameters.get(selected_goal, 
                                     {"sets": 3, "reps": "10-12", "rest": "1-2 min"})

        # Get previously used exercises from session to avoid repetition
        session_history = request.session.get('workout_history', [])
        
        # Build muscle group objects
        muscle_objects = MuscleGroup.objects.filter(name__in=selected_muscles)
        
        # Score and select exercises
        all_scored_exercises = []
        
        for muscle in muscle_objects:
            exercises = Exercise.objects.filter(
                Q(primary_muscle=muscle) | Q(secondary_muscles=muscle)
            ).distinct()

            # Apply filters
            if selected_difficulty:
                exercises = exercises.filter(difficulty=selected_difficulty)
            if selected_goal:
                exercises = exercises.filter(goals__name=selected_goal)
            if selected_equipment:
                exercises = exercises.filter(equipment__name=selected_equipment)

            # Score each exercise
            for exercise in exercises:
                score = calculate_exercise_score(
                    exercise, 
                    muscle, 
                    selected_goal,
                    session_history
                )
                all_scored_exercises.append({
                    'exercise': exercise,
                    'muscle': muscle,
                    'score': score,
                    'is_compound': exercise.mechanics == 'compound',
                    'is_primary': muscle in exercise.primary_muscle.all()
                })

        # Sort by score
        all_scored_exercises.sort(key=lambda x: x['score'], reverse=True)

        # Smart exercise selection
        selected_exercises = smart_exercise_selection(
            all_scored_exercises,
            muscle_objects,
            workout_params['total_exercises'],
            workout_params['exercises_per_muscle']
        )

        # Order exercises intelligently (compounds first, then isolations)
        ordered_exercises = order_exercises_optimally(selected_exercises)

        # Group by muscle for display
        workout_by_muscle = defaultdict(list)
        for idx, ex_data in enumerate(ordered_exercises, 1):
            exercise_info = {
                'exercise': ex_data['exercise'],
                'sets': params['sets'],
                'reps': params['reps'],
                'rest': params['rest'],
                'order': idx,
                'notes': generate_exercise_notes(ex_data['exercise'], selected_goal)
            }
            workout_by_muscle[ex_data['muscle'].name].append(exercise_info)

        # Update session history
        new_history = [ex['exercise'].id for ex in ordered_exercises]
        request.session['workout_history'] = (session_history + new_history)[-20:]  # Keep last 20

        # Calculate total volume estimate
        total_volume = estimate_total_volume(ordered_exercises, params)

        return render(
            request,
            "workouts/workout_results.html",
            {
                "workout": dict(workout_by_muscle),
                "goal": selected_goal,
                "length": selected_length,
                "total_exercises": len(ordered_exercises),
                "estimated_duration": estimate_workout_duration(ordered_exercises, params),
                "total_volume": total_volume,
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


def calculate_exercise_score(exercise, target_muscle, goal, history):
    """Score exercise based on multiple factors"""
    score = 0
    
    # Primary muscle match (highest priority)
    if target_muscle in exercise.primary_muscle.all():
        score += 50
    else:
        score += 20  # Secondary muscle match
    
    # Compound exercises generally better
    if exercise.mechanics == 'compound':
        score += 30
    else:
        score += 15
    
    # Goal alignment
    if goal and exercise.goals.filter(name=goal).exists():
        score += 25
    
    # Variety bonus (penalize recently used exercises)
    if exercise.id in history[-10:]:  # Last 10 exercises
        score -= 30
    elif exercise.id in history:
        score -= 15
    
    # Difficulty appropriateness (prefer intermediate for most)
    if exercise.difficulty == 'intermediate':
        score += 10
    
    return score


def smart_exercise_selection(scored_exercises, muscles, total_limit, per_muscle_limit):
    """Select exercises ensuring balance and variety"""
    selected = []
    muscle_counts = defaultdict(int)
    
    # First pass: Ensure at least one compound per muscle
    for ex_data in scored_exercises:
        if ex_data['is_compound'] and ex_data['is_primary']:
            muscle = ex_data['muscle']
            if muscle_counts[muscle.id] == 0:
                selected.append(ex_data)
                muscle_counts[muscle.id] += 1
    
    # Second pass: Fill remaining slots with best-scored exercises
    for ex_data in scored_exercises:
        if ex_data in selected:
            continue
            
        muscle = ex_data['muscle']
        if (len(selected) < total_limit and 
            muscle_counts[muscle.id] < per_muscle_limit):
            selected.append(ex_data)
            muscle_counts[muscle.id] += 1
    
    return selected


def order_exercises_optimally(exercises):
    """Order exercises: compounds first, then isolations"""
    compounds = [ex for ex in exercises if ex['is_compound']]
    isolations = [ex for ex in exercises if not ex['is_compound']]
    
    # Shuffle within categories for variety
    random.shuffle(compounds)
    random.shuffle(isolations)
    
    return compounds + isolations


def generate_exercise_notes(exercise, goal):
    """Generate helpful notes for each exercise"""
    notes = []
    
    if exercise.mechanics == 'compound':
        notes.append("Focus on form and control")
    
    if goal == 'strength':
        notes.append("Use challenging weight, prioritize form")
    elif goal == 'hypertrophy':
        notes.append("Focus on mind-muscle connection")
    elif goal == 'endurance':
        notes.append("Maintain steady pace, minimal rest")
    
    return " | ".join(notes) if notes else ""


def estimate_total_volume(exercises, params):
    """Estimate total volume (sets × reps)"""
    avg_reps = sum(map(int, params['reps'].split('-'))) / 2
    return int(len(exercises) * params['sets'] * avg_reps)


def estimate_workout_duration(exercises, params):
    """Estimate workout duration in minutes"""
    # Rough estimate: 45 sec per set + rest time
    rest_map = {"30-60 sec": 0.75, "1-2 min": 1.5, "3-5 min": 4}
    avg_rest = rest_map.get(params['rest'], 1.5)
    
    time_per_exercise = params['sets'] * (0.75 + avg_rest)
    total_minutes = int(len(exercises) * time_per_exercise)
    
    return f"{total_minutes} minutes"