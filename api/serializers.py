from rest_framework import serializers
from django.conf import settings
from properties.models import Property
from users.models import MaintenanceRequest
from payments.models import Payment
from notifications.models import Notification
from users.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL if False else CustomUser
        model = CustomUser
        fields = ('id','username','email','role','phone_number')

class PropertySerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ('owner','created_at')

class MaintenanceSerializer(serializers.ModelSerializer):
    tenant = UserSerializer(read_only=True)
    class Meta:
        model = MaintenanceRequest
        fields = '__all__'
        read_only_fields = ('tenant','created_at','updated_at')

class PaymentSerializer(serializers.ModelSerializer):
    tenant = UserSerializer(read_only=True)
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('tenant','status','created_at','confirmed_at')

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('user','created_at')
