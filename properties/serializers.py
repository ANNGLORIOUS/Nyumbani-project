from rest_framework import serializers

from .models import Inquiry, Property, PropertyImage
from users.serializers import UserSerializer


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ('id', 'image', 'caption', 'is_cover', 'created_at')
        read_only_fields = ('created_at',)


class PropertySerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    images = PropertyImageSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ('owner', 'created_at')


class InquirySerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Inquiry
        fields = '__all__'
        read_only_fields = ('sender', 'created_at', 'property')
