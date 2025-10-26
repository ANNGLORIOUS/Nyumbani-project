from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('tenant', 'Tenant'),
        ('owner', 'Owner'),
        ('caretaker', 'Caretaker'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='tenant')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    id_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
