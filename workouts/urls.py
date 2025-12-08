from django.urls import path

from . import views

urlpatterns = [
    path("", views.workout_generator_page, name="workout_generator_page"),
    path("workouts/workout_generator/", views.workout_generator, name="workout_generator"),
    path("workouts/advanced_workout_generator/", views.advanced_workout_generator, name="advanced_workout_generator"),
    path('save-workout/', views.save_workout, name='save_workout'),
path("workouts/saved/<int:workout_id>/", views.view_saved_workout, name="view_saved_workout"),

]