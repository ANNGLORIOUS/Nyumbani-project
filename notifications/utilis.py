import africastalking
from django.conf import settings

africastalking.initialize(
    settings.AFRICASTALKING_USERNAME, settings.AFRICASTALKING_API_KEY
)

sms = africastalking.SMS


def send_sms(phone_number, message):
    """
    Send SMS to a given phone number via Africa's Talking.
    """
    try:
        response = sms.send(message, [phone_number])
        print("✅ SMS sent:", response)
        return response
    except Exception as e:
        print("❌ Error sending SMS:", str(e))
        return None
