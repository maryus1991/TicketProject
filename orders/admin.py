from django.contrib import admin
from .models import Advertising, Order, UserWallet

# Register your models here.

admin.site.register(Advertising)
admin.site.register(Order)
admin.site.register(UserWallet)


