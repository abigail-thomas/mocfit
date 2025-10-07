from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('',  views.my_achievements, name="my_achievements"),
]