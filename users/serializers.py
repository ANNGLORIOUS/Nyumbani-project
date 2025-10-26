# users/serializers.py
from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'phone_number')
        read_only_fields = ('id',)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'role', 'phone_number')
        extra_kwargs = {'role': {'required': True}}

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        # optional: validate role value explicitly
        role = data.get('role')
        allowed = [c[0] for c in getattr(User, 'ROLE_CHOICES', User._meta.get_field('role').choices)]
        if role not in allowed:
            raise serializers.ValidationError({"role": "Invalid role."})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def to_representation(self, instance):
        """
        Return created user + JWT tokens.
        """
        data = UserSerializer(instance).data
        refresh = RefreshToken.for_user(instance)
        data['tokens'] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return data
