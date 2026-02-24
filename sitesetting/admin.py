from django.contrib import admin
from .models import Contact, Site, Team

# Register your models here.

admin.site.register(Team)
admin.site.register(Site)
admin.site.register(Contact)
