from django.urls import path

from . import views

urlpatterns = [
    path("", views.workout_generator_page, name="workout_generator_page"),
    path("workout_generator/", views.workout_generator, name="workout_generator"),
    path("advanced_workout_generator/", views.advanced_workout_generator, name="advanced_workout_generator"),
]