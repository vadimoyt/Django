from rest_framework import serializers

from trainer.models import Trainer
from .models import Training, Exercise, TrainingPlan, TrainingResult, Reminder


class TrainingSerializer(serializers.ModelSerializer):
    trainer = serializers.PrimaryKeyRelatedField(queryset=Trainer.objects.all())

    class Meta:
        model = Training
        fields = [
            'id',
            'title',
            'type',
            'level',
            'duration',
            'description',
            'trainer',
            'public'
        ]
        read_only_fields = ['id']


class ExerciseSerializer(serializers.ModelSerializer):
     class Meta:
        model = Exercise
        fields = ['id', 'training', 'title', 'description', 'amount_sets', 'repetitions']


class TrainingPlanSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    training = TrainingSerializer()

    class Meta:
        model = TrainingPlan
        fields = ['id', 'user', 'training', 'start_date', 'end_date', 'complete']


class TrainingResultSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    training = TrainingSerializer()

    class Meta:
        model = TrainingResult
        fields = ['id', 'user', 'training', 'date', 'notes', 'duration_minutes', 'burned_calories']


class ReminderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    training = TrainingSerializer()

    class Meta:
        model = Reminder
        fields = ['id', 'user', 'training', 'remind_at', 'sent']