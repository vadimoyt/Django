from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICE = [
        ('guest', 'Guest'),
        ('trainer', 'Trainer'),
        ('client', 'Client'),
    ]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICE,
        default='guest'
    )
