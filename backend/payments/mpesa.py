# payments/mpesa.py
import base64
from datetime import datetime
import uuid

import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth


def _has_live_credentials():
    return all([
        settings.MPESA_CONSUMER_KEY,
        settings.MPESA_CONSUMER_SECRET,
        settings.MPESA_SHORTCODE,
        settings.MPESA_PASSKEY,
    ])

def get_access_token():
    if settings.MPESA_SIMULATE or not _has_live_credentials():
        return "simulated-access-token"

    url = f"{settings.MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
    r = requests.get(
        url,
        auth=HTTPBasicAuth(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET),
        timeout=settings.MPESA_TIMEOUT,
    )
    r.raise_for_status()
    return r.json()['access_token']

def lipa_na_mpesa(phone_number, amount, account_reference="NyumbaniRent", transaction_desc="Rent Payment"):
    if settings.MPESA_SIMULATE or not _has_live_credentials():
        return {
            "ResponseCode": "0",
            "ResponseDescription": "Simulated STK push request accepted.",
            "CheckoutRequestID": f"SIM-{uuid.uuid4().hex[:12].upper()}",
            "CustomerMessage": "Simulation mode enabled.",
        }

    access_token = get_access_token()
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(
        (settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + timestamp).encode('utf-8')
    ).decode('utf-8')

    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://myapp.com/api/payments/mpesa/callback/",
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc
    }

    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{settings.MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest"
    response = requests.post(url, json=payload, headers=headers, timeout=settings.MPESA_TIMEOUT)
    response.raise_for_status()
    return response.json()
