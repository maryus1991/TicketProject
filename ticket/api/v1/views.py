from .serializers import TicketCategoryModelSerializers, SalonTicketModelSerializers, SalonGalleryModelSerializers, SalonModelSerializers, SalonUpdateModelSerializers
from ticket.models import Salon, SalonGallery, TicketCategory, SalonTicket
from rest_framework.generics import RetrieveAPIView, ListAPIView,  RetrieveUpdateAPIView, UpdateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView
from .pagination import CustomPagination
from django.utils.timezone import now
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

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


class SalonUpdateView(RetrieveUpdateAPIView):
    """
    for edit and update salon infos by its admin
    user obj equal to login and the sender of request user
    """

    permission_classes = [IsAuthenticated]
    serializer_class = SalonUpdateModelSerializers

    def get_queryset(self):
        return self.request.user.salon
    
    def get_object(self):
        return self.get_queryset()
    


class GallerySalonList(ListAPIView):
    """
    for list the galley of the salon
    return the active gallery when not auth ant not the salon admin request
    when the user logged in and the user is the admin of the salon its return active and not active galleries
    pk is salon id
    """

    serializer_class = SalonGalleryModelSerializers
    pagination_class = CustomPagination

    def get_queryset(self): 
        if not self.request.user.is_authenticated:
            return Salon.objects.filter(pk=self.kwargs.get('pk')).first().gallery.filter(is_active=True).all()
         
        user = self.request.user
        salon = Salon.objects.filter(pk=self.kwargs.get('pk'), admin=user)

        if salon.exists():
            return salon.first().gallery.all()

        else:
            return Salon.objects.filter(pk=self.kwargs.get('pk')).first().gallery.filter(is_active=True).all()
        

class GalleryRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    for list the galley of the salon
    return the active gallery when not auth ant not the salon admin request
    when the user logged in and the user is the admin of the salon its return active and not active galleries
    pk is salon id
    image_id for image id

     
    """

    serializer_class = SalonGalleryModelSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self): 
        user = self.request.user
        salon = Salon.objects.filter(pk=self.kwargs.get('pk'), admin=user)

        if salon.exists():
            return salon.first().gallery.all()

        else:
            return Response(
                'request user is not admin of the salon'
                ,status=status.HTTP_406_NOT_ACCEPTABLE
            )

    def get_object(self):
        return self.get_queryset().filter(pk=self.kwargs.get('image_id')).first()     
    

class CreateGallery(GenericAPIView):
    """
    for create gallery for salon
    """

    serializer_class = SalonGalleryModelSerializers
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        salon = Salon.objects.filter(admin=request.user)

        if not salon.exists() and salon.count() != 1:
            return Response(
                'obj not found', 
                status=status.HTTP_404_NOT_FOUND
            )
        
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        data.save()
        return Response(
            'gallery add successfully '
            ,status=status.HTTP_201_CREATED
        )
        