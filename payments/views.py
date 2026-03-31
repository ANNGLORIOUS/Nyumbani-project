# payments/views.py
import os
from django.conf import settings
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import generics
from .models import Payment
from .mpesa import lipa_na_mpesa  # your existing mpesa helper
from notifications.utilis import send_sms
from .serializers import PaymentSerializer

# ---------- initiate_payment ----------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    """
    Trigger STK push and create Payment record (status=pending).
    Expects: { "phone": "2547XXXXXXX", "amount": 10, "property": <id> }
    """
    phone = request.data.get('phone')
    amount = request.data.get('amount')
    property_id = request.data.get('property')

    if not phone or not amount:
        return Response({"error": "phone and amount required"}, status=400)

    # Create DB record first (pending)
    payment = Payment.objects.create(
        tenant=request.user,
        property_id=property_id,
        amount=amount,
        status='pending'
    )

    # Call Daraja (or simulate). Expect response with CheckoutRequestID
    try:
        mpesa_resp = lipa_na_mpesa(phone_number=phone, amount=amount,
                                  account_reference=f"payment_{payment.id}",
                                  transaction_desc="Nyumbani Rent")
    except Exception as e:
        payment.status = 'failed'
        payment.save()
        return Response({"error": "Failed to contact M-Pesa", "detail": str(e)}, status=500)

    # Real Daraja resp contains 'CheckoutRequestID' when ResponseCode == '0'
    checkout_id = mpesa_resp.get('CheckoutRequestID') or mpesa_resp.get('CheckoutRequestID', None)
    # Some sandbox responses put CheckoutRequestID inside result
    if not checkout_id:
        # attempt to read commonly nested fields
        checkout_id = mpesa_resp.get('data', {}).get('CheckoutRequestID') if isinstance(mpesa_resp, dict) else None

    # Save transaction id (if present) so callback can find it
    if checkout_id:
        payment.transaction_id = checkout_id
        payment.save()

    return Response({
        "payment_id": payment.id,
        "mpesa_response": mpesa_resp
    })


# ---------- mpesa_callback ----------
@api_view(['POST'])
@permission_classes([AllowAny])  # external system will call; we protect using header
def mpesa_callback(request):
    """
    Safaricom will POST here with Body -> stkCallback structure.
    We require a custom header for additional security: X-MPESA-SECRET
    """
    # quick header check
    secret_header = request.headers.get('X-MPESA-SECRET')
    expected = getattr(settings, 'MPESA_CALLBACK_SECRET', None)
    if expected:
        if secret_header != expected:
            return Response({"error": "Unauthorized callback"}, status=403)

    payload = request.data
    stk = payload.get('Body', {}).get('stkCallback', {})
    result_code = stk.get('ResultCode')
    checkout_id = stk.get('CheckoutRequestID')
    merchant_request_id = stk.get('MerchantRequestID')
    # you may want to parse amount from Callback metadata in a prod flow

    if not checkout_id:
        # fallback: maybe the payload structure is different in your test - log
        print("mpesa_callback: missing CheckoutRequestID", payload)

    payment = Payment.objects.filter(transaction_id=checkout_id).first()
    if result_code == 0:
        # success
        if payment:
            payment.status = 'confirmed'
            payment.confirmed_at = timezone.now()
            payment.save()
            # send SMS to tenant
            tenant_phone = payment.tenant.phone_number
            if tenant_phone:
                send_sms(
                    tenant_phone,
                    f"✅ Nyumbani: payment of Ksh {payment.amount} confirmed. Txn: {checkout_id}"
                )
        else:
            print("mpesa_callback: payment not found for checkout_id:", checkout_id)
        return Response({"ResultCode": 0, "ResultDesc": "Payment confirmed processed"}, status=200)
    else:
        # failed or cancelled
        if payment:
            payment.status = 'failed'
            payment.save()
            # optional: send SMS failure notice
            tenant_phone = payment.tenant.phone_number
            if tenant_phone:
                send_sms(
                    tenant_phone,
                    f"❌ Nyumbani: your payment attempt failed (Txn: {checkout_id}). Please try again."
                )
        return Response({"ResultCode": 0, "ResultDesc": "Processed (failed/cancelled)"}, status=200)
    

class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # tenants see their payments, owners maybe see payments for their properties
        if user.role == 'tenant':
            return Payment.objects.filter(tenant=user).order_by('-created_at')
        if user.role == 'owner':
            return Payment.objects.filter(property__owner=user).order_by('-created_at')
        return Payment.objects.none()
