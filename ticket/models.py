from django.db import models

from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Ticket(models.Model):
    """
    Tickets Model
    """
    

    name = models.CharField(max_length=255, verbose_name='نام بلیت')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ساخت')
    date_of_departure = models.DateTimeField(verbose_name='تاریخ حرکت')
    count_ofـpassengers = models.PositiveSmallIntegerField(verbose_name='تعداد مسافران')
        

    def __str__(self):
        return self.name


class PassengerPlacement(models.Model):
    """
    for detact the placement of passenger
    """
    
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name="بلیت")
    is_free = models.BooleanField(default=True, verbose_name="وضعیت خالی بودن :")
    passenger = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_index=True, verbose_name="مسافر")

    def __str__(self):
        return f"ticket : {self.ticket.name} -> {self.is_free}"



