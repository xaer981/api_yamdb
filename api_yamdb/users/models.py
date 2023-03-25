from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
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
        verbose_name='отображаемое имя',
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='username содержит недопустимый символ'
        )]
    )

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='электронная почта'
    )

    first_name = models.CharField(
        max_length=150, verbose_name='имя', blank=True
    )

    last_name = models.CharField(
        max_length=150, verbose_name='фамилия', blank=True
    )

    bio = models.TextField(verbose_name='биография', blank=True)

    role = models.CharField(
        max_length=15,
        default=USER,
        choices=ROLE_CHOICE,
        verbose_name='роль'
    )

    class Meta:
        ordering = ('id',)

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moder(self):
        return self.role == self.MODERATOR
