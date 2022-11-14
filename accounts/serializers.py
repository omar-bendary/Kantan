from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from .models import User


class ForgetPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)


class VerfiyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=50)


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=50)


class OTPGetSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):

        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
        )

        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):

        if user.is_verified:
            token = super().get_token(user)
            # token['phone_number'] = str(user.phone_number)
            return token

        elif not user.is_verified:
            raise serializers.ValidationError("User is Not verified")
