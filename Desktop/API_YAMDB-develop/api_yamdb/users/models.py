from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE_CHOICES = [
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
]


class MyUser(AbstractUser):
    """Кастомная модель пользователя."""
    email = models.EmailField('Email адрес', unique=True, blank=False)
    role = models.CharField(
        'Роль',
        max_length=10,
        choices=ROLE_CHOICES,
        default='user'
    )
    bio = models.TextField('Биография', blank=True)
    confirmation_code = models.CharField('Код подтверждения', max_length=6,
                                         blank=True)

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
