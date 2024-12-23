from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from user.models import CustomUser


class Trainer(models.Model):
    first_name = models.CharField(
        max_length=20,
        null=False
    )
    last_name = models.CharField(
        max_length=20,
        null=False
    )
    years = models.IntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(45)],
        null=False
    )
    year_of_exp = models.IntegerField(
        validators=[MinValueValidator(2), MaxValueValidator(27)],
        null=False
    )
    bio = models.TextField(
        max_length=250,
        null=True
    )

    def __str__(self):
        return (f"First name: {self.first_name}. \n"
                f"Last name: {self.last_name}. \n"
                )


class RatingOfTrainer(models.Model):
    trainer = models.ForeignKey(
        Trainer,
        verbose_name='Trainer',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        CustomUser,
        verbose_name='User',
        on_delete=models.CASCADE
    )
    rating = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=False
        )
    review = models.TextField(
        null=True,
        max_length=500
        )
    date = models.DateField(auto_now=True, verbose_name='Time of review')

    class Meta:
        unique_together = ('trainer', 'user')

    def __str__(self):
        return (f'Review by {self.user.username} '
                f'for {self.trainer.first_name} {self.trainer.last_name}'
                f' - {self.rating}/10')



