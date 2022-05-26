import graphene
from graphene import relay, ObjectType, Mutation
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from fitness.models import Exercise, Workout, Cycle, Category, OneRepMax, WorkoutLog, Measurements

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('id', 'name')
        
class ExerciseType(DjangoObjectType):
    class Meta:
        model = Exercise
        fields = ('id', 'name','body_part')
        
class WorkoutType(DjangoObjectType):
    class Meta:
        model = Workout
        fields = ('id', 'name', 'category')
        
class CycleType(DjangoObjectType):
    class Meta:
        model = Cycle
        fields = ('id', 'name', 'workouts')
        
class OneRepMaxType(DjangoObjectType):
    class Meta:
        model = OneRepMax
        fields = ('id', 'exercise', 'user')
        
class WorkoutLogType(DjangoObjectType):
    class Meta:
        model = WorkoutLog
        fields = ('id', 'user', 'workout', 'exercise')
        
class MeasurementsType(DjangoObjectType):
    class Meta:
        model = Measurements
        fields = ('id', 'user', 'measurementDate')
        
class Query(ObjectType):
    all_categories = graphene.List(CategoryType)
    all_exercises = graphene.List(ExerciseType)
    all_user_workouts = graphene.List(WorkoutType, user_id=graphene.Int())
    all_user_measurements = graphene.List(MeasurementsType, user_id=graphene.Int())
    all_user_one_reps = graphene.List(OneRepMaxType, user_id=graphene.Int())
    logs_by_user_and_workout = graphene.List(WorkoutLogType, user_id=graphene.Int(), workout_id=graphene.Int())
    
    def resolve_all_categories(self, info):
        return Category.objects.all()
    def resolve_all_exercises(self, info):
        return Exercise.objects.all()
    def resolve_all_user_workouts(self, info, user_id):
        return Workout.objects.filter(user=user_id)
    def resolve_all_user_measurements(self, info, user_id):
        return Measurements.objects.filter(user=user_id)
    def resolve_all_user_one_reps(self, info, user_id):
        return OneRepMax.objects.filter(user=user_id)
    def resolve_logs_by_user_and_workout(self, info, user_id, workout_id):
        return WorkoutLog.objects.filter(user=user_id, workout=workout_id)

class CatergoryMutation(Mutation):
    class Arguments:
        text = graphene.String()
        id = graphene.ID()
        description = graphene.String()
        
    categoryMutation = graphene.Field(CategoryType)
        
    def mutate(cls, root, info, text, description, id):
        if id:
            category = Category.objects.get(pk=id)
            category.name = text
            category.description = description
            category.save()
            return CatergoryMutation(category=category)
        else:
            category = Category.objects.create(name=text, description=description)
            return CatergoryMutation(category=category)
        
class ExerciseMutation(Mutation):
    class Arguments:
        text = graphene.String()
        id = graphene.ID()
        body_part = graphene.String()
        
    exerciseMutation = graphene.Field(ExerciseType)
        
    def mutate(cls, root, info, text, body_part, id):
        if id:
            exercise = Exercise.objects.get(pk=id)
            exercise.name = text
            exercise.body_part = body_part
            exercise.save()
            return ExerciseMutation(exercise=exercise)
        else:
            exercise = Exercise.objects.create(name=text, body_part=body_part)
            return ExerciseMutation(exercise=exercise)
        
class WorkoutMutation(Mutation):
    class Arguments:
        text = graphene.String()
        id = graphene.ID()
        category = graphene.ID()
        
    workoutMutation = graphene.Field(WorkoutType)
    
    def mutate(cls, root, info, text, category, id):
        if id:
            workout = Workout.objects.get(pk=id)
            workout.name = text
            workout.category = Category.objects.get(pk=category)
            workout.save()
            return WorkoutMutation(workout=workout)
        else:
            workout = Workout.objects.create(name=text, category=Category.objects.get(pk=category))
            return WorkoutMutation(workout=workout)
        
class CycleMutation(Mutation):
    class Arguments:
        text = graphene.String()
        id = graphene.ID()
        workouts = graphene.List(graphene.ID)
        
    cycleMutation = graphene.Field(CycleType)
    
    def mutate(cls, root, info, text, workouts, id):
        if id:
            cycle = Cycle.objects.get(pk=id)
            cycle.name = text
            cycle.workouts = Workout.objects.filter(pk__in=workouts)
            cycle.save()
            return CycleMutation(cycle=cycle)
        else:
            cycle = Cycle.objects.create(name=text, workouts=Workout.objects.filter(pk__in=workouts))
            return CycleMutation(cycle=cycle)
        
class OneRepMaxMutation(Mutation):
    class Arguments:
        exercise = graphene.ID()
        user = graphene.ID()
        weight = graphene.Float()
        reps = graphene.Int()
        id = graphene.ID()
        
    onerepmaxMutation = graphene.Field(OneRepMaxType)
    
    def mutate(cls, root, info, exercise, user, weight, reps, id):
        if id:
            onerepmax = OneRepMax.objects.get(pk=id)
            onerepmax.exercise = Exercise.objects.get(pk=exercise)
            onerepmax.user = User.objects.get(pk=user)
            onerepmax.weight = weight
            onerepmax.reps = reps
            onerepmax.save()
            return OneRepMaxMutation(onerepmax=onerepmax)
        else:
            onerepmax = OneRepMax.objects.create(exercise=Exercise.objects.get(pk=exercise), user=User.objects.get(pk=user), weight=weight, reps=reps)
            return OneRepMaxMutation(onerepmax=onerepmax)
        
class WorkoutLogMutation(Mutation):
    class Arguments:
        workout = graphene.ID()
        exercise = graphene.ID()
        user = graphene.ID()
        id = graphene.ID()
        
    workoutlogMutation = graphene.Field(WorkoutLogType)
    
    def mutate(cls, root, info, workout, exercise, user, id):
        if id:
            workoutlog = WorkoutLog.objects.get(pk=id)
            workoutlog.workout = Workout.objects.get(pk=workout)
            workoutlog.exercise = Exercise.objects.get(pk=exercise)
            workoutlog.user = User.objects.get(pk=user)
            workoutlog.save()
            return WorkoutLogMutation(workoutlog=workoutlog)
        else:
            workoutlog = WorkoutLog.objects.create(workout=Workout.objects.get(pk=workout), exercise=Exercise.objects.get(pk=exercise), user=User.objects.get(pk=user))
            return WorkoutLogMutation(workoutlog=workoutlog)

class Mutation(ObjectType):
    category = CatergoryMutation.Field()
    exercise = ExerciseMutation.Field()
    workout = WorkoutMutation.Field()
    cycle = CycleMutation.Field()
    onerepmax = OneRepMaxMutation.Field()
    workoutlog = WorkoutLogMutation.Field()