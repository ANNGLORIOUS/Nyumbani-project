from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone

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
    print("📩 M-Pesa callback received:", request.data)
    return Response({"ResultCode": 0, "ResultDesc": "Accepted"})
