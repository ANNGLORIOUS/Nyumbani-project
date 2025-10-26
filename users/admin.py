from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, TenantProfile, MaintenanceRequest


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('role', 'phone_number', 'id_number')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info', {'fields': ('role', 'phone_number', 'id_number')}),
    )

    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')

admin.site.register(TenantProfile)
admin.site.register(MaintenanceRequest)
