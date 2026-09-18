from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .cutome_user_manager import CustomUserManager

class User(AbstractBaseUser,PermissionsMixin):
    user_name=None
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    objects = CustomUserManager()
    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default= False)
    is_superuser = models.BooleanField(default= False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

