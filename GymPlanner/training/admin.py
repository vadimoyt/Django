from django.contrib import admin

from .models import Exercise, Training

class TrainingAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_exercises', )

    def get_exercises(self, obj):
        return ', '.join([exercises.title for exercises in obj.exercises.all()])

    get_exercises.short_description = 'Exercises'
admin.site.register(Exercise)
admin.site.register(Training, TrainingAdmin)
