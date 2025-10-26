from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Notification(models.Model):
    NOTIF_TYPE = [('sms', 'sms'), ('email','email'), ('system','system')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPE, default='system')
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
