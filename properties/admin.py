from django.contrib import admin
from .models import Inquiry, Property, PropertyImage

admin.site.register(Property)
admin.site.register(Inquiry)
admin.site.register(PropertyImage)
