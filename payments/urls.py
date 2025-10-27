from django.urls import path
from .views import initiate_payment, mpesa_callback

urlpatterns = [
    path('mpesa/pay/', initiate_payment, name='mpesa-pay'),
    path('mpesa/callback/', mpesa_callback, name='mpesa-callback'),
]
