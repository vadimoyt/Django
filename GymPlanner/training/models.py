from django.db.models import CASCADE

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from trainer.models import Trainer

class Exercise(models.Model):
    title = models.CharField(max_length=20, null=False)
    description = models.TextField(max_length=1500, null=False)
    amount_sets = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=False
    )
    repetitions = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(250)],
        null=False
    )

    def __str__(self):
        return self.title


class Training(models.Model):
    CHOICE_TYPE = [
        ('power', 'Power'),
        ('cardio', 'Cardio'),
        ('flexibility', 'Flexibility'),
        ('balance', 'Balance'),
    ]
    CHOICE_LEVEL = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    title = models.CharField(
        max_length=50,
        null=False
    )
    type = models.CharField(
        choices=CHOICE_TYPE,
        null=False
    )
    level = models.CharField(
        choices=CHOICE_LEVEL,
        null=False
    )
    duration = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(365)],
        null=False
    )
    description = models.TextField(
        max_length=250,
        null=False
    )
    exercises = models.ManyToManyField(Exercise)
    trainer = models.ForeignKey(Trainer, on_delete=CASCADE, null=False)

    def __str__(self):
        return (
            f"Training: {self.title}. "
            f"Type: {self.type}. "
            f"Level: {self.level}. "
            f"Duration(days): {self.duration}. "
            f"Description: {self.description}. "
            f"Exercise: {self.exercises}. "
            f"Trainer: {self.trainer.first_name}"
        )
