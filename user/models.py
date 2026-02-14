from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.timezone import timedelta, now
from random import randint
from utils.send_otp import send_otp
from .managers import UserManager

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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ثبت نام')
    
    USERNAME_FIELD = "PhoneNumber"
    EMAIL_FIELD = "PhoneNumber"

    objects = UserManager()

    def __str__(self):
        return f"{str(self.PhoneNumber).replace(' ', '')}"
    
    def set_otp(self) -> int:
 
        self.otp_expiry_date = now() + timedelta(minutes=2)
        self.otp = randint(100000, 999999)
        self.save()

        try:
            send_otp.delay(
                str(self.PhoneNumber).replace(" ", ""),
                self.otp
            )
        except Exception as e:
            print(self.__class__.__name__, e)

        return self.otp

    def verify_otp(self, otp: str) -> bool:

        if (int(self.otp) == int(otp)) and (self.otp_expiry_date >= now()):
            self.otp = ""
            self.otp_expiry_date = None
            self.save()
            return True
        else:
            return False
