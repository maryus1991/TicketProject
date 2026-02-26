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

class SalonUpdateModelSerializers(serializers.ModelSerializer):
    """
    serializer for update salon 
    """
    
    class Meta:
        model = Salon
        fields = [
            'name',
            'address',
            'logo',
            'description',
            'support_phone_number',
            'create_at',
            'working_hours_start',
            'working_hours_end',
            'accepted_gender',
            'location',
            'is_active',
            'sort_number',
            'accept_ticket_cancelling',
        ]

    def update(self, instance, validated_data):
        validated_data.update({
            'admin': self.context['request'].user
        })
        instance.admin = self.context['request'].user
        return super().update(instance, validated_data)
 
class SalonTicketModelSerializers(serializers.ModelSerializer):
    """
    serializer for ticket 
    """
    
    class Meta:
        model = SalonTicket
        fields = '__all__'