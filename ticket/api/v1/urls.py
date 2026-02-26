from django.urls import path
from .views import ( 
    CategoriesListView, 
    SalonListView, 
    SalonRetrieveView, 
    SalonTicketListView, 
    SalonUpdateView, 
    GallerySalonList, 
    GalleryRetrieveUpdateDeleteView,
    CreateGallery
)

app_name='tickets'

urlpatterns = [
    path('categories/', CategoriesListView.as_view(), name='categories-list'),
    path('salon/', SalonListView.as_view(), name='salon-list'),
    path('salon/<int:pk>/', SalonRetrieveView.as_view(), name='salon-retrieve'),
    path('categories/<int:pk>/tickets/', SalonTicketListView.as_view(), name='ticket-list'),
    path('ticket/', SalonTicketListView.as_view(), name='ticket-list'),
    path('salon/update/', SalonUpdateView.as_view()),
    path('salon/<int:pk>/gallery-list', GallerySalonList.as_view()),
    path('salon/<int:pk>/gallery-list/<int:image_id>', GalleryRetrieveUpdateDeleteView.as_view()),
    path('salon/create-gallery', CreateGallery.as_view()),
]
