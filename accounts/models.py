
import datetime
from random import randint
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from .otp import otp
from .send_sms import send_sms

my_otp = otp()


class UserProfileManager(BaseUserManager):

    def create_user(self, phone_number, password=None, **kwargs):

        if not phone_number:
            raise ValueError('Users must have a number')

        user = self.model(phone_number=phone_number, **kwargs)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number,  password, **kwargs):
        user = self.create_user(phone_number, password)

        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = PhoneNumberField(unique=True, null=False, blank=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()
    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return str(self.phone_number)


class OTP(models.Model):
    code = models.CharField(max_length=6, primary_key=True)
    user = models.ForeignKey(User, related_name='OTPs',
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    is_expired = models.BooleanField(default=False)
    reset_password_permission = models.BooleanField(default=False)

    def __str__(self):
        return self.code


@receiver(post_save, sender=get_user_model())
def create_user_otp(sender, instance, created, **kwargs):
    if created:
        otp = OTP.objects.create(user=instance, code=randint(100000, 999999))
        user = User.objects.get(OTPs=otp)
        try:
            send_sms(number=str(user.phone_number), OTP=otp.code)
        except:
            pass
