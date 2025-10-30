from django.contrib import admin
from .models import Achievement, UserAchievement, UserProfile

# Register your models here.
admin.site.register(Achievement)
admin.site.register(UserAchievement)
admin.site.register(UserProfile)