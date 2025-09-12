from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "home"),
    path("<str:workout_type>/", views.generate, name = "generate"),
]