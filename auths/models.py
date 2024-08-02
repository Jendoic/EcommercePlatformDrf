from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .userManager import MyUserManager
from django.conf import settings
from django.utils import timezone
from django.db.models import Sum



class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, null=True, blank=True)

    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = MyUserManager()
    REQUIRED_FIELDS = ['name']
    USERNAME_FIELD = "email"
    EMAIL_FIELD = 'email'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

