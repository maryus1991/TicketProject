from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.gis.db.models.fields import PointField 
 
from django.utils.crypto import get_random_string
import os

# Create your models here.

User = get_user_model()

def photo_path_upload_to(instance, filename):
    basename = os.path.basename(filename)
    return f"logo/{get_random_string(100)}-{basename}"

class SalonGenderAccept(models.TextChoices):
    """
    for detact the gender of users 
    """
    MALE = "M", 'مذکر'
    FELMALE = "F", "مونث" 
    BOTH = "B", "هردو" 


class Salon(models.Model):
    """
    Tickets Model
    """
    
    admin = models.ForeignKey(User, verbose_name='ادمین', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255, verbose_name='نام سالون')
    address = models.TextField(verbose_name='ادرس')
    logo = ThumbnailerImageField(upload_to=photo_path_upload_to, verbose_name='لوگو')
    description = models.TextField(verbose_name='توضیحات')
    support_phone_number = PhoneNumberField(verbose_name='شماره تلفن پشتیبان')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ساخت')
    working_hours_start = models.TimeField(verbose_name='شروع ساعت کاری ') 
    working_hours_end = models.TimeField(verbose_name='پایان ساعت کاری ') 
    accepted_gender = models.CharField(verbose_name='جنسیت مورد قبول', choices=SalonGenderAccept) 
    location = PointField(verbose_name='موقعیت', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='وضعیت')
    sort_number = models.PositiveSmallIntegerField(default=0, verbose_name='عدد اولویت بندی (هر چه بزرگتر بالاتر نمایش داده می شود)')

    class Meta:
        verbose_name = 'سالون '
        verbose_name_plural = 'سالون ها'

    def __str__(self):
        return self.name


def salon_gallery_photo_path_upload_to(instance, filename):
    basename = os.path.basename(filename)
    return f"galley/salon/{get_random_string(100)}-{basename}"


class SalonGallery(models.Model):
    image = ThumbnailerImageField(upload_to=salon_gallery_photo_path_upload_to, verbose_name='عکس')
    sort_number = models.PositiveSmallIntegerField(default=0, verbose_name='عدد اولویت بندی (هر چه بزرگتر بالاتر نمایش داده می شود)')
    is_active = models.BooleanField(default=True, verbose_name='وضعیت')
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='gallery')

    class Meta:
        verbose_name = 'عکس '
        verbose_name_plural = 'گالری'

    def __str__(self):
        return str(self.id)

def category_photo_path_upload_to(instance, filename):
    basename = os.path.basename(filename)
    return f"categories/logo/{get_random_string(100)}-{basename}"


class TicketCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام دسته')
    logo = ThumbnailerImageField(upload_to=category_photo_path_upload_to, verbose_name='لوگو')
    is_active = models.BooleanField(default=True, verbose_name='وضعیت')
    sort_number = models.PositiveSmallIntegerField(default=0, verbose_name='عدد اولویت بندی (هر چه بزرگتر بالاتر نمایش داده می شود)')


    class Meta:
        verbose_name = 'دسته '
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.name


class SalonTicket(models.Model):
    category = models.ForeignKey(TicketCategory, verbose_name='دسته', on_delete=models.CASCADE)
    salon = models.ForeignKey(Salon, verbose_name='سالون', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, verbose_name='وضعیت')
    accepted_gender = models.CharField(verbose_name='جنسیت مورد قبول', choices=SalonGenderAccept) 
    working_datetime_start = models.DateTimeField(verbose_name='شروع ساعت کاری ') 
 
    price = models.PositiveBigIntegerField(verbose_name='قیمت')
    capacity = models.PositiveSmallIntegerField(verbose_name='ظرفیت', default=1)
    current_capacity = models.PositiveSmallIntegerField(verbose_name=' فعلی ظرفیت', default=1)
    name = models.CharField(max_length=255, verbose_name='نام')
    sort_number = models.PositiveSmallIntegerField(default=0, verbose_name='عدد اولویت بندی (هر چه بزرگتر بالاتر نمایش داده می شود)')

    class Meta:
        verbose_name = 'بلیت '
        verbose_name_plural = 'بلیت'

    def __str__(self):
        return self.name


