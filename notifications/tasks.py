from celery import shared_task
from django.utils import timezone

from .models import Notification
from .utilis import send_sms

@shared_task
def deliver_sms(notification_id):
    notification = Notification.objects.select_related('user').get(pk=notification_id)
    if notification.delivery_status == 'sent':
        return {'status': 'already_sent'}
    response = send_sms(notification.user.phone_number, notification.message)
    if response.get('status') in ('failed', 'skipped'):
        notification.delivery_status = response['status']
        notification.delivery_error = response.get('reason', '')
    else:
        notification.delivery_status = 'sent'
        notification.sent_at = timezone.now()
    notification.save(update_fields=('delivery_status', 'delivery_error', 'sent_at'))
    return response
