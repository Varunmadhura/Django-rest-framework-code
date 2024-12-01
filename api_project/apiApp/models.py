from django.db import models
from django.utils import timezone


class Register(models.Model):
    username = models.CharField(max_length=254)
    email = models.CharField(max_length=254,unique=True)
    mobile = models.CharField(max_length=20)
    password = models.CharField(max_length=254)
    cfrm_password = models.CharField(max_length=254)

    
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


