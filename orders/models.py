from django.db import models
from user.models import User
from ticket.models import SalonTicket, Salon
from django.utils.crypto import get_random_string
from easy_thumbnails.fields import ThumbnailerImageField

import os

# Create your models here.

class OrderStatus(models.TextChoices):
    awaitingـpayment = 'awaitingـpayment', 'منتظر پرداخت'
    cancelled = 'cancelled', 'کنسل شده'
    awaiting_paid_to_admin = 'awaiting_paid_to_admin', 'منتظر پرداخت به ادمین'
    paid = 'paid', 'پرداخت شده'



class Order(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, verbose_name='سالون')
    user = models.ForeignKey(User, verbose_name='کاربر', on_delete=models.Case)
    wallet = models.ForeignKey('UserWallet', verbose_name='کیف پول', on_delete=models.PROTECT)
    ticket = models.ForeignKey(SalonTicket, verbose_name='بلیت', on_delete=models.SET_NULL, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ افزودن')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='تایخ پرداخت')
    status = models.CharField(verbose_name='وضعیت', choices=OrderStatus, default=OrderStatus.awaitingـpayment, max_length=255)
    price = models.PositiveBigIntegerField(verbose_name='قیمت تاریخ چه', null=True, blank=True)
    payment_code = models.PositiveBigIntegerField(verbose_name='کد پیگیری', null=True, blank=True)

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'

    def __str__(self): return f'سفارش شماره {self.id} برای کاربر { str(self.user.PhoneNumber).replace(" ", "") } '


class WalletStatus(models.TextChoices):
    awaiting = 'awaiting', 'در حالت انتظار'
    return_request = 'return_request', 'درخواست برداشت'
    paid = 'paid', 'پرداخت شده'

class UserWallet(models.Model):
    user = models.ForeignKey(User, verbose_name='کاربر', on_delete=models.PROTECT, related_name='wallet')
    price = models.PositiveBigIntegerField(verbose_name='قیمت', default=0)
    status = models.CharField(max_length=255, choices=WalletStatus, default=WalletStatus.awaiting, verbose_name='وضعیت') 

    def __str__(self): return f'{str(self.user.PhoneNumber).replace(" ","")}'


    class Meta:
        verbose_name = 'کیف پول'
        verbose_name_plural = 'کیف پول'

def photo_path_upload_to(instance, filename):
    basename = os.path.basename(filename)
    return f"advertising/{get_random_string(100)}-{basename}"


class Advertising(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام')
    link = models.CharField(max_length=1000, verbose_name='لینک')
    image = ThumbnailerImageField(upload_to=photo_path_upload_to, verbose_name='عکس')
    description = models.TextField(verbose_name='توضیحات')
    is_active=models.BooleanField(default=True, verbose_name='وضعیت')

    class Meta:
        verbose_name = 'تبلیغ'
        verbose_name_plural = 'تبلیغات'

    def __str__(self):
        return self.name