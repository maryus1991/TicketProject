from .serializer import AdvertisingModelSerializer, UserWalletModelSerializer, OrderCreateModelSerializer, OrderListModelSerializer
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order, SalonTicket, UserWallet, Advertising, Salon
from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from ticket.api.v1.pagination import CustomPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from sitesetting.models import Site
from django.utils.timezone import timedelta, now

User = get_user_model()


class SetOrderPostView(GenericAPIView):
    """
    for create Order for user
    send id of ticket 
    for user send the phone number
    403 code for full capacity 
    406 for gender not acceptable 
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


            if ticket.accepted_gender != 'B' and ticket.accepted_gender != user.gender:
                return Response('gender not acceptable', status=status.HTTP_406_NOT_ACCEPTABLE)

            
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
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['salon', 'wallet', 'ticket', 'payment_code']
    ordering_fields = ['status', 'create_at', 'paid_at', 'price', 'ticket']

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-status').all()
    

class SalonOrdersList(ListAPIView):
    """
    for list the salon paid tickets 
    for login salon admin 
    """

    serializer_class = OrderListModelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['salon__name','salon__id', 'wallet__status', 'ticket__id', 'payment_code']
    ordering_fields = ['status', 'create_at', 'paid_at', 'price', 'ticket__id', ]

    def get_queryset(self):
        user = self.request.user
        
        # if not hasattr(user, "salon"):
        #     return Order.objects.none()

        return Order.objects.filter(
            salon=user.salon,
            status='paid'
        ).order_by('-paid_at')


class UserCancelOrderBeforPayment(APIView):
    """
    for cancel the order by user before payment 
    send the id of the order 
    403 for obj not exists
    406 for time over that after the accepted time for cancelling
    202 for success
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('pk')
        order = Order.objects.filter(
            user = request.user,
            id = order_id,
            status= 'awaitingـpayment'
        )
        if not order.exists() or order.count() != 1:
            return Response(
                'error object not detacted', 
                status=status.HTTP_403_FORBIDDEN
            )
        
        order = order.first()
        minutes_to_allow_cancelling_the_order = Site.objects.first().minutes_to_allow_cancelling_the_order
        
        if order.ticket.working_datetime_start - timedelta(minutes=minutes_to_allow_cancelling_the_order) <= now():
            return Response(
                "time for cancelling finish out",
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

        order.status = 'cancelled'
        order.save()

        return Response(
            "order cancelled successfully",
            status=status.HTTP_202_ACCEPTED
        )


class UserCancelOrderAfterPayment(APIView):
    """
    for cancel the order by user after payment 
    send the id of the order 
    404 for not found obj 
    406 for not allowed to change 
    202 for success operation
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('pk')
        order = Order.objects.filter(
            user = request.user,
            id = order_id,
            status= 'paid'
        )
        if not order.exists() or order.count() != 1:
            return Response(
                'error object not detacted', 
                status=status.HTTP_404_NOT_FOUND
            )
        
        order = order.first()

        if not order.salon.accept_ticket_cancelling:
            return Response(
                "salon does not accept the cancelling after payment ",
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        minutes_to_allow_cancelling_the_order_after_payment = Site.objects.first().minutes_to_allow_cancelling_the_order_after_payment
        if order.ticket.working_datetime_start - timedelta(hours=minutes_to_allow_cancelling_the_order_after_payment) <= now():
            return Response(
                "time for cancelling  after payment hash been finish out",
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

        tiket_price = order.ticket.price
        salon_admin_wallet = order.salon.admin
        
        salon_admin_wallet = UserWallet.objects.get_or_create(
            user = salon_admin_wallet,
            status='awaiting'
        )[0]
        
        if salon_admin_wallet.price:
            salon_admin_wallet.price -= tiket_price
        else : 
            salon_admin_wallet.price = tiket_price

        salon_admin_wallet.save()

        user_wallet = UserWallet.objects.get_or_create(
            user = order.user,
            status='awaiting'
        )[0]

        if user_wallet.price:
            user_wallet.price += order.price
        else:
            user_wallet.price = order.price

        user_wallet.save()

        order.status = 'cancelled'
        order.save()

        return Response(
            "order cancelled successfully",
            status=status.HTTP_202_ACCEPTED
        )


        



