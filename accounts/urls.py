
from .views import RegisterAPI, ForgetPasswordAPI, VerifyOTPUser, VerifyOTPRsesrtPassword, RestPasswordAPI
from django.urls import path

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('verify-user/', VerifyOTPUser.as_view(), name='verify-user'),
    path('forget-password/', ForgetPasswordAPI.as_view(), name='forget-password'),
    path('verify-forgetpassword/',
         VerifyOTPRsesrtPassword.as_view(), name='verify-forgetpassword'),
    path('reset-password/', RestPasswordAPI.as_view(), name='reset-password'),

]
