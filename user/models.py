from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum
from .manager import UserManager


class GenderEnum(Enum):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(
        max_length=20,
        choices=[(tag.value, tag) for tag in GenderEnum],
        default=GenderEnum.MALE
    )
    password = models.CharField(max_length=500, null=False)
    email = models.EmailField(max_length=255, null=False, unique=True)
    phone = models.CharField(max_length=20, null=False)
    dob = models.DateField(null=True, blank=True)
    username = None
    address = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Changed related_name
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  # Changed related_name
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_query_name='user',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
