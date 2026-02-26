from ticket.models import TicketCategory, Salon, SalonGallery, SalonTicket
from rest_framework import serializers


class TicketCategoryModelSerializers(serializers.ModelSerializer):
    """
    serializer for categories 
    """

    class Meta:
        model = TicketCategory
        fields = '__all__'



class SalonGalleryModelSerializers(serializers.ModelSerializer):
    """
    serializer for gallery 
    """

    class Meta:
        model = SalonGallery
        fields = '__all__'

class SalonModelSerializers(serializers.ModelSerializer):
    """
    serializer for salon 
    """
    
    gallery = SalonGalleryModelSerializers(read_only=True, many=True)
    
    class Meta:
        model = Salon
        fields = '__all__'

 


class SalonTicketModelSerializers(serializers.ModelSerializer):
    """
    serializer for ticket 
    """
    
    class Meta:
        model = SalonTicket
        fields = '__all__'