from django.db import models

# Create your models here.

class Property(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    rent_price = models.DecimalField(max_digits=10, decimal_places=2)
    available_units = models.IntegerField(default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name