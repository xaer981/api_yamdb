from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель User с расширенными параметрами."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICE = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Отображаемое имя'
    )

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта'
    )

    first_name = models.CharField(
        max_length=150, verbose_name='Имя', blank=True
    )

    last_name = models.CharField(
        max_length=150, verbose_name='Фамилия', blank=True
    )

    bio = models.TextField(verbose_name='Биография', blank=True)

    role = models.CharField(
        max_length=15,
        default=USER,
        choices=ROLE_CHOICE,
        verbose_name='Роль'
    )

    class Meta:
        ordering = ('id',)
