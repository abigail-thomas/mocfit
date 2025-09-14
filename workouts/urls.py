from django.urls import path
from . import views

urlpatterns = [
    path("", views.workout_generator_page, name = "workout_generator_page"),
    path("<str:workout_type>/", views.workout_generator, name = "workout_generator"),
]