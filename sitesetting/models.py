from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from easy_thumbnails.fields import ThumbnailerImageField

from django.utils.crypto import get_random_string
import os

def photo_path_upload_to(instance, filename):
    basename = os.path.basename(filename)
    return f"site/{get_random_string(100)}-{basename}"


class Site(models.Model):
    name = models.CharField(max_length=255, verbose_name='عنوان')
    address = models.TextField(verbose_name='ادرس')
    logo = ThumbnailerImageField(upload_to=photo_path_upload_to, verbose_name='لوگو')
    description = models.TextField(verbose_name='توضیحات')
    support_phone_number = PhoneNumberField(verbose_name='شماره تلفن پشتیبان')
    site_tax = models.PositiveSmallIntegerField(verbose_name='مالیات زیر ساخت')

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات سایت'


    def __str__(self):
        return self.name
    

class Contact(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام')
    title = models.CharField(max_length=255, verbose_name='عنوان پیام')
    phone_number = PhoneNumberField(verbose_name='شماره تلفن ')
    description = models.TextField(verbose_name='توضیحات')
    is_active = models.BooleanField(default=True, verbose_name='پاسخ داده شده')


    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'تماس با ما'


    def __str__(self):
        return self.name + ' = ' + self.title


class Team(models.Model):
    name = models.CharField(max_length=255, verbose_name='عنوان')
    image = ThumbnailerImageField(upload_to=photo_path_upload_to, verbose_name='عکس')
    phone_number = PhoneNumberField(verbose_name='شماره تلفن ')
    email =  models.EmailField(max_length=255, verbose_name='ایمیل')
    link =  models.URLField(verbose_name='لینک')
    
    class Meta:
        verbose_name = 'تیم'
        verbose_name_plural = 'تیم'

    def __str__(self):
        return self.name



    



