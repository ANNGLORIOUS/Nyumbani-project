from django.contrib import admin

# Register your models here.
from .models import Payment
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'property', 'amount', 'transaction_id', 'status', 'created_at', 'confirmed_at')
    list_filter = ('status', 'created_at')
    search_fields = ('tenant__username', 'property__name', 'transaction_id')
    ordering = ('-created_at',) 
admin.site.register(Payment, PaymentAdmin)
