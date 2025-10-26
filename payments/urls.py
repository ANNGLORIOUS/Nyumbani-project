from django.urls import path
from . import views

urlpatterns = [
    path('mpesa/pay/', views.initiate_payment, name='mpesa-pay'),
    path('mpesa/callback/', views.mpesa_callback, name='mpesa-callback'),
]
