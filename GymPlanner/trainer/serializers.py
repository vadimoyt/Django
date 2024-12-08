from rest_framework import serializers
from .models import Trainer

class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = [
            'id',
            'first_name',
            'last_name',
            'years',
            'year_of_exp',
            'bio',
        ]