from django.contrib import admin
from fitness.models import Exercise, Workout, Cycle, Category, OneRepMax, WorkoutLog, Measurements
# Register your models here.
admin.site.register(Exercise)
admin.site.register(Workout)
admin.site.register(Cycle)
admin.site.register(Category)
admin.site.register(OneRepMax)
admin.site.register(WorkoutLog)
admin.site.register(Measurements)