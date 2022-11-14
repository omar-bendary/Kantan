
import datetime
from random import randint

from requests import request

from .models import OTP, User
from .serializers import ForgetPasswordSerializer, ResetPasswordSerializer, UserSerializer, RegisterSerializer, OTPGetSerializer, VerfiyOTPSerializer
from rest_framework.response import Response
from rest_framework import status
from .send_sms import send_sms
from rest_framework import generics
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.timezone import utc
from .otp import otp


my_otp = otp()


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class VerifyOTPUser(generics.GenericAPIView):
    serializer_class = OTPGetSerializer

    def get(self, *args, **kwargs):
        if self.request.user.id:
            return Response("hi")
        else:
            return Response("nah")

    def post(self, request, *args, **kwargs):
        current_user = request.user
        print('----------------')
        print(current_user.id)

        token_key = request.data['token']
        otp = request.data['code']
        token = AuthToken.objects.get(token_key=token_key[:8])
        user = User.objects.get(auth_token_set=token.digest)
        user_otp = OTP.objects.filter(user=user).first()

        diff_in_seconds = (datetime.datetime.utcnow().replace(
            tzinfo=utc)-user_otp.created_at).total_seconds()
        diff_in_minutes = diff_in_seconds/60

        if int(diff_in_minutes) > 10:

            user_otp.is_expired = True
            user_otp.save()

        if str(user_otp) == str(otp) and not user_otp.is_expired:
            user.is_verified = True
            user.save()
            return Response("User Verified", status=status.HTTP_201_CREATED)

        return Response("Worng OTP", status=status.HTTP_406_NOT_ACCEPTABLE)


class ForgetPasswordAPI(generics.GenericAPIView):
    serializer_class = ForgetPasswordSerializer

    def post(self, request, *args, **kwargs):
        phone_number = request.data['phone_number']

        try:
            user = User.objects.get(phone_number=phone_number)
            otp = OTP.objects.filter(user=user).update(
                code=randint(100000, 999999), is_expired=False, created_at=datetime.datetime.now())

            try:
                send_sms(number=str(user.phone_number), OTP=otp.code)
            except:
                pass

            return Response({
                "token": AuthToken.objects.create(user)[1]
            })
        except:
            return Response("No user with this phone number .")


class VerifyOTPRsesrtPassword(generics.GenericAPIView):
    serializer_class = VerfiyOTPSerializer

    def post(self, request, *args, **kwargs):
        token_key = request.data['token']
        otp = request.data['otp']
        token = AuthToken.objects.get(token_key=token_key[:8])
        user = User.objects.get(auth_token_set=token.digest)
        user_otp = OTP.objects.filter(user=user).last()

        diff_in_seconds = (datetime.datetime.utcnow().replace(
            tzinfo=utc)-user_otp.created_at).total_seconds()
        diff_in_minutes = diff_in_seconds/60

        if int(diff_in_minutes) > 10:

            user_otp.is_expired = True
            user_otp.save()

        if str(user_otp) == str(otp) and not user_otp.is_expired:
            user_otp.reset_password_permission = True
            user_otp.save()
            return Response("OTP Verified", status=status.HTTP_200_OK)

        return Response("Worng OTP", status=status.HTTP_406_NOT_ACCEPTABLE)


class RestPasswordAPI(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        token_key = request.data['token']
        password = request.data['password']
        token = AuthToken.objects.get(token_key=token_key[:8])
        user = User.objects.get(auth_token_set=token.digest)
        user_otp = OTP.objects.filter(user=user).last()

        diff_in_seconds = (datetime.datetime.utcnow().replace(
            tzinfo=utc)-user_otp.created_at).total_seconds()
        diff_in_minutes = diff_in_seconds/60

        if int(diff_in_minutes) > 10:

            user_otp.is_expired = True
            user_otp.save()

        if not user_otp.is_expired and user_otp.reset_password_permission:
            user.set_password(password)
            user.save()
            return Response("Password Reset successfully", status=status.HTTP_201_CREATED)

        return Response("Error Reseting the password", status=status.HTTP_406_NOT_ACCEPTABLE)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


#
