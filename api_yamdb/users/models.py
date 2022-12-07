from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )
    MAX_ROLE_LENGTH = len(max([i[0] for i in ROLE_CHOICES], key=len))
    username = models.SlugField(
        'Юзернейм',
        blank=False,
        unique=True,
        max_length=150,
    )
    first_name = models.CharField(
        'Имя',
        blank=True,
        unique=False,
        max_length=150,
    )
    last_name = models.CharField(
        'Фамилия',
        blank=True,
        unique=False,
        max_length=150,
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
        max_length=MAX_ROLE_LENGTH,
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER





    class Meta:
        ordering = ('role',)
