from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


class User(AbstractUser):
    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )
    password = models.CharField(
        'Пароль',
        max_length=50,
        blank=True
    )
    email = models.EmailField(
        'Электронная почта',
        blank=False,
        unique=True,
        max_length=254,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        choices=ROLE_CHOICES,
        default=USER,
        max_length=len(max([i[0] for i in ROLE_CHOICES], key=len)),
    )

    class Meta:
        ordering = ('role',)
