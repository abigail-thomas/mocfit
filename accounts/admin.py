from django.contrib import admin
from .models import Profile, WeightEntry

# Register your models here.
admin.site.register(Profile)
admin.site.register(WeightEntry)