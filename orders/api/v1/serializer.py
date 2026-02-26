from orders.models import Advertising, Order, UserWallet
from rest_framework import serializers
from user.api.v1.serializers import PhoneNumberSerializer2
from ticket.api.v1.serializers import SalonModelSerializers, SalonTicketModelSerializers
from ticket.models import SalonTicket

class AdvertisingModelSerializer(serializers.ModelSerializer):
    """
    serializer for advertising 
    """

    class Meta:
        model=Advertising
        fields='__all__'
        read_only_fields = ['id']
        

class UserWalletModelSerializer(serializers.ModelSerializer):
    """
    serializer for user wallet 
    """
    user = PhoneNumberSerializer2(read_only=True)
    class Meta:
        model=UserWallet
        fields='__all__'
        read_only_fields = ['id']
        

class OrderListModelSerializer(serializers.ModelSerializer):
    """serializer for order list"""

    user = PhoneNumberSerializer2(read_only=True)
    wallet = UserWalletModelSerializer(read_only=True)
    ticket = SalonTicketModelSerializers(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'salon',
            'wallet',
            'ticket',
            'price',
            'status',
            'create_at',
            'paid_at',
            'payment_code'
        ]
        read_only_fields = [
            'id',
            'salon',
            'user',
            'ticket',
            'wallet',
            'price',
            'status',
            'create_at',
            'paid_at',
            'payment_code'
        ]

class OrderCreateModelSerializer(serializers.ModelSerializer): 
    ticket = serializers.PrimaryKeyRelatedField(
        queryset=SalonTicket.objects.filter(is_active=True).all()
    )

    class Meta:
        model = Order
        fields = [
                
            'ticket',
        ]