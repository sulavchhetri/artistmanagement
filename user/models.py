from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=500, null=False)
    email = models.EmailField(max_length=255, null=False, unique=True)
    phone = models.CharField(max_length=20, null=False)
    dob = models.DateField()
    username = None
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

