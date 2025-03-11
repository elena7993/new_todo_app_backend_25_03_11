from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.


class User(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",  # ✅ 기존 'user_set'과 충돌 방지
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",  # ✅ 기존 'permission_set'과 충돌 방지
        blank=True,
    )

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
