from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id','property','rent_record','amount','status','transaction_id','created_at','confirmed_at']
