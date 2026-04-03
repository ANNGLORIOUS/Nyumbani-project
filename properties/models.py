from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Property(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_properties')
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=200)
    rent_price = models.DecimalField(max_digits=10, decimal_places=2)
    caretaker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='caretaken_properties')
    available_units = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.location}"


class Inquiry(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("closed", "Closed"),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="inquiries")
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_inquiries",
    )
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry for {self.property.name} by {self.name}"
