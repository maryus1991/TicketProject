from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.timezone import timedelta, now
from random import randint
from utils.send_otp import send_otp
from .managers import UserManager
from config.settings import OTP_EXPIRATIONS_MINUTES
# Create your models here.

class GenderOfPassengers(models.TextChoices):
    """
    for detact the gender of passengers 
    """
    MALE = "M", 'مذکر'
    FELMALE = "F", "مونث" 


class User(AbstractUser):
    """
     User model
    """
    
    gender = models.CharField(max_length=255, choices=GenderOfPassengers, verbose_name="جنسیت")
    PhoneNumber = PhoneNumberField(unique=True, db_index=True, verbose_name="شماره")
    otp = models.CharField(max_length=6, blank=True, null=True, verbose_name="کد otp")
    otp_expiry_date = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ انقضای ")

    is_active = models.BooleanField(default=True, verbose_name='فعال بودن')
    is_verified = models.BooleanField(default=True, verbose_name='تایید اطلاعات')
    login_request = models.BooleanField(default=False, verbose_name='درخواست لاگین')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ثبت نام')
    
    USERNAME_FIELD = "PhoneNumber"
    EMAIL_FIELD = "PhoneNumber"

    objects = UserManager()

    def __str__(self):
        return f"{str(self.PhoneNumber).replace(' ', '')}"
    
    def set_otp(self) -> int:
 
        self.otp_expiry_date = now() + timedelta(minutes=int(OTP_EXPIRATIONS_MINUTES))
        self.otp = randint(100000, 999999)
        self.login_request = True
        self.save()

        return self.otp

    def verify_otp(self, otp: str) -> bool:

        if (int(self.otp) == int(otp)) and (self.otp_expiry_date >= now()):
            self.otp = ""
            self.otp_expiry_date = None
            self.login_request = False
            self.save()
            return True
        else:
            return False
