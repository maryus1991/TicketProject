from django.contrib import admin
from .models import Salon, SalonGallery, SalonTicket, TicketCategory

admin.site.register(Salon)
admin.site.register(SalonGallery)
admin.site.register(SalonTicket)
admin.site.register(TicketCategory)