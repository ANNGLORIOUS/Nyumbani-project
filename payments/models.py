from django.conf import settings
from django.db import models
from properties.models import Property

User = settings.AUTH_USER_MODEL

class Payment(models.Model):
    STATUS = [('pending','pending'), ('confirmed','confirmed'), ('failed','failed')]

    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=128, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
