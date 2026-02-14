from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from utils.send_otp import send_otp

@receiver(post_save, sender=User)
def send_otp_when_user_create(sender, instance: User, created, **kwargs):
    if instance.login_request: 
        send_otp(
            str(instance.PhoneNumber).replace(' ',''),
            instance.otp,
        )