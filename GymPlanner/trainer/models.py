from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


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
                f"Age: {self.years}. \n"
                f"Experience: {self.year_of_exp} years. \n"
                f"BIO: {self.bio}.")