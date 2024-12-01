from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from apps.account.managers.auth_manager import CustomUserManager
from django.utils.translation import gettext as _


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=15, null=True, blank=True, unique=True, verbose_name="Телефон")
    email = models.EmailField(unique=True, verbose_name="Электронная почта", null=True, blank=True)
    username = models.CharField(max_length=15, null=True, blank=True, unique=True, verbose_name="Логин")
    first_name = models.CharField(max_length=30, verbose_name="Имя", null=True, blank=True)
    last_name = models.CharField(max_length=30, verbose_name="Фамилия", null=True, blank=True)
    city = models.CharField(max_length=100, verbose_name="Город", null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name=_("Аватар"))
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_staff = models.BooleanField(default=False, verbose_name="Персонал")

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.first_name} ({self.last_name})"

