from django.db import models
from django.contrib.auth.models import AbstractUser

CHOICES = (
    ('admin', 'Администратор'),
    ('moderator', 'Модератор'),
    ('user', 'Пользователь'),
)


class User(AbstractUser):
    email = models.EmailField('Почта', unique=True, max_length=254)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль',
        max_length=20, choices=CHOICES, default=CHOICES[2]
    )
