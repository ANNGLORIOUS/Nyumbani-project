from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Notification(models.Model):
    NOTIF_TYPE = [('sms', 'sms'), ('email','email'), ('system','system')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPE, default='system')
    read = models.BooleanField(default=False)
    delivery_status = models.CharField(max_length=20, default='pending')
    delivery_error = models.TextField(blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
