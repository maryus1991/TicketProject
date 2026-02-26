from .serializer import AdvertisingModelSerializer, UserWalletModelSerializer, OrderCreateModelSerializer, OrderListModelSerializer
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order, SalonTicket, UserWallet, Advertising
from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from ticket.api.v1.pagination import CustomPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from sitesetting.models import Site
User = get_user_model()

class SetOrderPostView(GenericAPIView):
    """
    for create Order for user
    send id of ticket 
    for user send the phone number
    403 code for full capacity 
    201 for succcess order 

    """
    serializer_class = OrderCreateModelSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        ticket = data.validated_data.get('ticket')
        user = request.user
        

        with atomic():    
            salon_admin_wallet = UserWallet.objects.get_or_create(
                user=ticket.salon.admin,
                status='awaiting'
            )[0]

            if ticket.current_capacity >= ticket.capacity:
                return Response('capacity is full', status=status.HTTP_403_FORBIDDEN)

            
            order = Order.objects.get_or_create(
                user = user,
                ticket=ticket,
                salon = ticket.salon,
                wallet=salon_admin_wallet,
                status='awaitingـpayment',
                payment_code__isnull=True

            )[0]

            ## calc the price
            ticket_price = ticket.price
            order.price = ticket_price + (ticket_price * (Site.objects.first().site_tax / 100))
            order.save()

             

        return Response(OrderListModelSerializer(order).data, status=status.HTTP_201_CREATED)

            
class AdvertisingListView(ListAPIView):

    """
    for listing the advertising
    """

    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['id']
    serializer_class = AdvertisingModelSerializer
    queryset = Advertising.objects.filter(is_active=True).all()


class WalletListing(ListAPIView):
    """
    for listing the 
    """
    serializer_class = UserWalletModelSerializer
    permission_classes = [IsAuthenticated]

    
    def get_queryset(self):
        return UserWallet.objects.filter(
            user=self.request.user
        ).order_by('status').all()
        

class WalletChangeStatusToPaidRequest(GenericAPIView):
    """
    just send the id of the wallet and it will change it to paid request
    202 for success
    404 for not found error
    """
    serializer_class = UserWalletModelSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        wallet = UserWallet.objects.filter(
            user = self.request.user,
            id=kwargs.get('pk'),
            status='awaiting'
        )

        if not wallet.exists() or wallet.count() != 1:
            return Response('obj not found', status=status.HTTP_404_NOT_FOUND)
        
        wallet = wallet.first()

        wallet.status = 'return_request'
        wallet.save()
        return Response('paid request has been send to admin', status=status.HTTP_202_ACCEPTED)
    

class OrderListView(ListAPIView):
    """
    for listing the orders 
    """
    serializer_class = OrderListModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('create_at').all()
    

