from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'user'),
        (ADMIN, 'admin'),
    ]
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
        blank=False,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=False,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=False,
    )
    password = models.CharField(
        'Пароль',
        max_length=150,
        blank=False,
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True,
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'username',
                    'email'
                ],
                name='unique_user',
            )
        ]

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    def __str__(self):
        return f'{self.username}'


class Subscribe(models.Model):
    follow = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='follow',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='На кого подписываются',
        related_name='author',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Подписка',
        verbose_name_plural = 'Подписки',
        constraints = (
            models.UniqueConstraint(
                fields=[
                    'follow',
                    'author'
                ],
                name='unique_subscribe'
            ),
        )

    def __str__(self):
        return f"{self.follow} подписан на {self.author}"
