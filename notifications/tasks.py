from celery import shared_task
from .sms import send_sms

@shared_task
def send_rent_reminder(phone_number, message):
    send_sms(phone_number, message)
