from django.urls import path
from .views import CategoriesListView, SalonListView, SalonRetrieveView, SalonTicketListView

app_name='tickets'

urlpatterns = [
    path('categories/', CategoriesListView.as_view(), name='categories-list'),
    path('salon/', SalonListView.as_view(), name='salon-list'),
    path('salon/<int:pk>/', SalonRetrieveView.as_view(), name='salon-retrieve'),
    path('categories/<int:pk>/tickets/', SalonTicketListView.as_view(), name='ticket-list'),
    path('ticket/', SalonTicketListView.as_view(), name='ticket-list'),
]
