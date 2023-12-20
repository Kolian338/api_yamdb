from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class UserRoles(models.TextChoices):
        ADMIN = "admin", _("Администратор")
        MODERATOR = "moderator", _("Модератор")
        USER = "user", _("Пользователь")

    email = models.EmailField('Почта', unique=True, max_length=254)
    bio = models.TextField('Биография', blank=True, null=True)
    role = models.CharField(
        'Роль',
        max_length=20, choices=UserRoles.choices, default=UserRoles.USER
    )

    def __str__(self):
        return self.username
