from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role & Contact Info', {'fields': ('role', 'phone_number', 'id_number')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
