from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)
from django.db import models


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""
        user = self.model(email=email, **extra_fields)
        user.email = self.normalize_email(email)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    objects = UserManager()
