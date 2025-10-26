from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from properties.models import Property

User = settings.AUTH_USER_MODEL


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
    
class TenantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tenant_profile')
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True, related_name='tenants')
    move_in_date = models.DateField(null=True, blank=True)
    rent_due_day = models.PositiveSmallIntegerField(default=1)  # e.g., 1..28

    def __str__(self):
        return f"Tenant: {self.user.username}"
    
class MaintenanceRequest(models.Model):
    ISSUE_TYPES = [
        ('plumbing', 'Plumbing'),
        ('electrical', 'Electrical'),
        ('wifi', 'Wi-Fi'),
        ('other', 'Other'),
    ]
    STATUS = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='maintenance_requests')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='maintenance_requests')
    issue_type = models.CharField(max_length=40, choices=ISSUE_TYPES, default='other')
    description = models.TextField()
    status = models.CharField(max_length=30, choices=STATUS, default='pending')
    caretaker_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
