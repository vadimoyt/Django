from rest_framework import serializers

from trainer.models import Trainer
from .models import Training

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
            'exercises',
            'trainer',
        ]
        read_only_fields = ['id']