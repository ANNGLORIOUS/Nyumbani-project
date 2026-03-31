from django.urls import path
from .views import initiate_payment, mpesa_callback, PaymentListView

urlpatterns = [
    path('mpesa/pay/', initiate_payment, name='mpesa-pay'),
    path('mpesa/callback/', mpesa_callback, name='mpesa-callback'),
    path('history/', PaymentListView.as_view(), name='payment-history'),

]
