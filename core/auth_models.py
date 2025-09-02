import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.db import models


class CustomUserManager(UserManager):
    def create_user(self, phone, password=None, **extra_fields):
        user = self.model(
            phone=phone,
            password=password,
            **extra_fields
        )
        user.set_password(str(password))
        user.save()
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        return self.create_user(
            phone=phone, password=password,
            is_staff=True, is_superuser=True, **extra_fields)

    def get_admins(self):
        return self.get_queryset().filter(user_type=2)

    def get_users(self):
        return self.get_queryset().filter(user_type=1)


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=15, unique=True)
    username = models.CharField(max_length=56)
    user_type = models.SmallIntegerField(default=1, choices=[
        (1, "User"),
        (2, "Admin"),
    ])

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username', "user_type"]

    # class Meta:
    #


class Otp(models.Model):
    key = models.CharField(max_length=256, primary_key=True, unique=True)  # shifr
    mobile = models.CharField(max_length=15)

    tries = models.SmallIntegerField(default=0)
    is_expired = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    extra_fields = models.JSONField(default=dict)
    next_step = models.CharField(default='step2', choices=[
        ("step2", "step2"),
        ("regis", "regis"),
        ("login", "login"),
    ])

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.tries >= 3:
            self.is_expired = True
        return super(Otp, self).save(*args, **kwargs)

    def check_time(self):
        now = datetime.datetime.now()
        calc = (now-self.created).total_seconds()
        if calc > 180:
            return False
        return True





