from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from notifications.utilis import send_sms
from .models import Payment

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    phone = request.data.get('phone')
    amount = request.data.get('amount')

    # fake M-Pesa simulation (for now)
    print(f"Simulating M-Pesa payment: {phone} -> KES {amount}")
    
    return Response({
        "CustomerMessage": "Payment initiated successfully",
        "ResponseCode": "0",
        "MerchantRequestID": "SIM123",
        "CheckoutRequestID": "CHK456",
    })

@api_view(['POST'])
def mpesa_callback(request):
    data = request.data.get("Body", {}).get("stkCallback", {})
    result_code = data.get("ResultCode")
    checkout_id = data.get("CheckoutRequestID")

    payment = Payment.objects.filter(transaction_id=checkout_id).first()

    if result_code == 0:
        if payment:
            payment.status = "confirmed"
            payment.confirmed_at = timezone.now()
            payment.save()

            # ✅ Send SMS confirmation
            tenant_phone = payment.tenant.phone_number
            amount = payment.amount
            send_sms(
                tenant_phone,
                f"✅ Payment of Ksh {amount} confirmed. Thank you for paying via Nyumbani!"
            )

        return Response({"message": "Payment confirmed and SMS sent"}, status=200)

    else:
        if payment:
            payment.status = "failed"
            payment.save()
        return Response({"message": "Payment failed"}, status=400)