from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):

    first_name = models.CharField(
        max_length=150,
        editable=False,
    )

    last_name = models.CharField(
        max_length=150,
        editable=False,
    )

    name = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    avatar = models.URLField(
        null=True,
        blank=True,
    )
