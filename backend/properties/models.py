from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Property(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_properties')
    name = models.CharField(max_length=150)
    property_type = models.CharField(max_length=50, default='apartment')
    location = models.CharField(max_length=200)
    county = models.CharField(max_length=100, blank=True)
    neighborhood = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    rent_price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveSmallIntegerField(default=0)
    bathrooms = models.PositiveSmallIntegerField(default=0)
    amenities = models.JSONField(default=list, blank=True)
    STATUS_CHOICES = [('available', 'Available'), ('unavailable', 'Unavailable'), ('draft', 'Draft')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    caretaker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='caretaken_properties')
    available_units = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.location}"


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property-images/')
    caption = models.CharField(max_length=200, blank=True)
    is_cover = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-is_cover', 'created_at')

    def __str__(self):
        return f"Image for {self.property.name}"


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
