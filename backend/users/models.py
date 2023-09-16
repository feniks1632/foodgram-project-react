from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    user = 'user', 'Пользователь'
    admin = 'admin', 'Администратор'

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = models.CharField(
        'Пользователь',
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        'электронная Почта',
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        'Имя пользователя',
        max_length=150,
    )
    last_name = models.CharField(
        'Фамилия пользователя',
        max_length=150,
    )
    password = models.CharField(
        'Пароль',
        max_length=150
    )
    role = models.CharField(
        'Роль пользователя',
        choices=Role.choices,
        max_length=20,
        default=Role.user
    )
    is_block = models.BooleanField(
        'Заблокированный',
        default=False
    )

    REQUIRED_FIELDS = [
        'email',
        'first_name',
        'last_name'
    ]

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Follow(models.Model):
    follow = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='follow',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='author',
    )

    def __str__(self):
        return f"{self.follow} подписан на {self.author}"

    class Meta:
        ordering = ['id']
        verbose_name = 'Подписчик',
        verbose_name_plural = 'Подписчики',
        constraints = (
            models.UniqueConstraint(
                fields=['follow', 'author'],
                name='unique_recording'
            ),
        )

        def __str__(self):
            return f'{self.follow} подписан на: {self.author}'
