import logging
import os

from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

try:
    import africastalking
except ImportError:  # pragma: no cover - exercised indirectly in environments without the package
    africastalking = None


def _get_sms_client():
    sms_enabled = getattr(settings, "SMS_ENABLED", os.getenv("SMS_ENABLED", "false").lower() in ("1", "true", "yes", "on"))
    username = os.getenv("AFRICASTALKING_USERNAME")
    api_key = os.getenv("AFRICASTALKING_API_KEY")
    if not sms_enabled or not africastalking or not username or not api_key:
        return None

    africastalking.initialize(username, api_key)
    return africastalking.SMS


def send_sms(phone, message):
    sms_client = _get_sms_client()
    if not sms_client:
        logger.warning("SMS skipped because Africa's Talking is not configured.")
        return {"status": "skipped", "reason": "sms_not_configured"}

    try:
        response = sms_client.send(message, [phone])
        logger.info("SMS sent successfully to %s", phone)
        return response
    except Exception as exc:  # pragma: no cover - network/provider failure
        logger.warning("SMS sending failed for %s: %s", phone, exc)
        return {"status": "failed", "reason": str(exc)}
