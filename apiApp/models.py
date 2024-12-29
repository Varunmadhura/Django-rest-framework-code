from django.db import models
from django.utils import timezone

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class RegisterManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('This Email field is required')
        email=self.normalize_email(email)
        user =self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email,password, **extra_fields)

class Register(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=254)
    email = models.CharField(max_length=254, unique=True)
    mobile = models.CharField(max_length=20)
    password = models.CharField(max_length=264)
    cfrm_password = models.CharField(max_length=264)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = RegisterManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email







class Login(models.Model):
    email = models.CharField(max_length=254)
    password = models.CharField(max_length=254)


class CommandExecutingLog(models.Model):
    hostname = models.CharField(max_length=254)
    username = models.CharField(max_length=254)
    password = models.CharField(max_length=254)
    command = models.TextField()
    output = models.TextField(null=True, blank=True)
    error = models.TextField(null=True, blank=True)
    executed_at = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


