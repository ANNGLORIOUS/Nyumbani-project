from django.shortcuts import render

# Create your views here.
from notifications.sms import send_sms

send_sms("+254712345678", "Your rent payment was received successfully.")

