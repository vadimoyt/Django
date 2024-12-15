from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CASCADE
from rest_framework.exceptions import ValidationError

from trainer.models import Trainer
from user.models import CustomUser


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
        null=False,
        max_length=20
    )
    level = models.CharField(
        choices=CHOICE_LEVEL,
        null=False,
        max_length=20
    )
    duration = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(365)],
        null=False
    )
    description = models.TextField(
        max_length=250,
        null=False
    )
    trainer = models.ForeignKey(
        Trainer,
        on_delete=CASCADE,
        null=False
    )
    public = models.BooleanField(
        default=True,
        verbose_name='Is training is public?'
    )

    def __str__(self):
        return (
            f"Training: {self.title}. "
            f"Type: {self.type}. "
            f"Level: {self.level}. "
            f"Duration(days): {self.duration}. "
            f"Description: {self.description}. "
            f"Exercise: {' '.join([exercise.title for exercise in self.exercises.all()])}. "
            f"Trainer: {self.trainer.first_name}"
        )



class Exercise(models.Model):
    training = models.ForeignKey(
        Training,
        on_delete=models.CASCADE,
        related_name='exercises',
        verbose_name='training',
        null=True
    )
    title = models.CharField(
        max_length=20,
        null=False
    )
    description = models.TextField(
        max_length=1500,
        null=False
    )
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


class TrainingPlan(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='training_plans',
        verbose_name='User'
    )
    training = models.ForeignKey(
        Training,
        on_delete=models.CASCADE,
        related_name='assigned_plan',
        verbose_name='Training'
    )
    start_date = models.DateField(verbose_name='Date of the beginning')
    end_date = models.DateField(verbose_name='Date of end')
    complete = models.BooleanField(
        default=False,
        verbose_name='Is completed?'
    )

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError('Start date must be earlier than end date.')

    def __str__(self):
        return f'Plan for {self.user.username} - {self.training.title}'


class TrainingResult(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='training_result',
        verbose_name='User'
    )
    training = models.ForeignKey(
        Training,
        on_delete=models.CASCADE,
        verbose_name='Training'
    )
    date = models.DateField(verbose_name='Date of training')
    notes = models.TextField(
        blank=True,
        verbose_name='Notes'
    )
    duration_minutes = models.PositiveSmallIntegerField(verbose_name='Duration of training in minutes')
    burned_calories = models.PositiveIntegerField(
        verbose_name='Burned calories',
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(5000)]
    )

    def __str__(self):
        return f'Result of {self.user.username} - for {self.training.title} on {self.date}'


class Reminder(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reminders',
        verbose_name="User"
    )
    training = models.ForeignKey(
        'Training',
        on_delete=models.CASCADE,
        verbose_name="Training"
    )
    remind_at = models.DateTimeField(verbose_name="Date and time of reminder")
    sent = models.BooleanField(
        default=False,
        verbose_name="Has remind sent?"
    )

    def __str__(self):
        return f"Reminder for {self.user.username} about {self.training.title} at {self.remind_at}"