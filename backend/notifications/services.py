"""The sole entry point for application notifications.

Domain apps create a durable notification first; SMS delivery is delegated to a
Celery task only after the surrounding database transaction commits.
"""
from django.conf import settings
from django.db import transaction

from .models import Notification
from .tasks import deliver_sms


def notify(user, message, notif_type='sms'):
    notification = Notification.objects.create(
        user=user, message=message, notif_type=notif_type,
        delivery_status='pending' if notif_type == 'sms' else 'not_applicable',
    )
    if notif_type == 'sms' and user.phone_number:
        transaction.on_commit(lambda: queue_sms(notification.pk))
    elif notif_type == 'sms':
        notification.delivery_status = 'skipped'
        notification.delivery_error = 'Recipient has no phone number.'
        notification.save(update_fields=('delivery_status', 'delivery_error'))
    return notification


def queue_sms(notification_id):
    """Queue delivery when a broker is configured; otherwise retain the record.

    This makes local development safe and avoids a web request making an SMS API
    call or failing because Redis/Celery is not running.
    """
    if not getattr(settings, 'NOTIFICATIONS_ASYNC', False):
        return
    deliver_sms.delay(notification_id)
