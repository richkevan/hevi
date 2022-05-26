from sqlite3 import Date
from unicodedata import category
from django.db import models

# Create your models here.
class Exercise(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='exercises/')
    video = models.URLField()
    body_part = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class Workout(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    exercises = models.ManyToManyField(Exercise)
    
    def __str__(self):
        return self.name
    
class Cycle(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    workouts = models.ManyToManyField(Workout)
    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class OneRepMax(models.Model):
    exercise = models.ForeignKey('Exercise', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    weight = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.exercise.name + " " + str(self.weight)
    
class WorkoutLog(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    workout = models.ForeignKey('Workout', on_delete=models.CASCADE)
    exercise = models.ForeignKey('Exercise', on_delete=models.CASCADE)
    sets = models.IntegerField()
    reps = models.IntegerField()
    weight = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.workout.name + " " + self.exercise.name + " " + str(self.sets) + "x" + str(self.reps)
    
class Measurements(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    weight = models.IntegerField()
    chest = models.IntegerField()
    waist = models.IntegerField()
    hips = models.IntegerField()
    measurementDate = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.user) + "Measurements"