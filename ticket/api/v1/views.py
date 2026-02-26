from .serializers import TicketCategoryModelSerializers, SalonTicketModelSerializers, SalonGalleryModelSerializers, SalonModelSerializers
from ticket.models import Salon, SalonGallery, TicketCategory, SalonTicket
from rest_framework.generics import RetrieveAPIView, GenericAPIView, ListAPIView
from .pagination import CustomPagination
from django.utils.timezone import now
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch

class CategoriesListView(ListAPIView):
    """
    for listing the categories
    """

    queryset = TicketCategory.objects.filter(is_active=True).order_by('-sort_number').all()
    serializer_class = TicketCategoryModelSerializers
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name', 'id']
    search_fields = ['name', 'id']


class SalonTicketListView(ListAPIView):
    """
    for listing the ticket 
    send pk (category id) if you want to get ticket with that category 
    """
    model = SalonTicket
    serializer_class = SalonTicketModelSerializers
    pagination_class = CustomPagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = {
        'category': ['exact'],
        'salon': ['exact'],
        'accepted_gender': ['exact'],

        # فیلتر بازه تاریخ
        'working_datetime_start': ['gte', 'lte'],

        # فیلتر بازه قیمت
        'price': ['gte', 'lte'],

        # ظرفیت حداقل/حداکثر
        'capacity': ['gte', 'lte'],
    }

    search_fields = ['name']

    ordering_fields = ['price', 'working_datetime_start', 'capacity']


    def get_queryset(self):
        queryset = SalonTicket.objects.prefetch_related('salon','category').filter(is_active=True, working_datetime_start__gte=now())

        category_id = self.kwargs.get('pk')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset.order_by('-sort_number', 'working_datetime_start')


class SalonListView(ListAPIView):
    """
    salon list view
    """
    serializer_class = SalonModelSerializers
    pagination_class = CustomPagination
 
    queryset = Salon.objects.prefetch_related(
        Prefetch(
            'gallery',
            queryset=SalonGallery.objects.filter(
                is_active=True
            ).order_by('-sort_number')
        )
    ).order_by('-sort_number').all()


class SalonRetrieveView(RetrieveAPIView):

    '''
    salon detail view
    '''

    serializer_class = SalonModelSerializers
    pagination_class = CustomPagination
    queryset = Salon.objects.prefetch_related(
        Prefetch(
            'gallery',
            queryset=SalonGallery.objects.filter(
                is_active=True
            ).order_by('-sort_number')
        )
    ).order_by('-sort_number').all()
