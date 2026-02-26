from django.urls import path
from .views import SetOrderPostView, AdvertisingListView,WalletListing, WalletChangeStatusToPaidRequest, OrderListView

urlpatterns = [
    path('create/', SetOrderPostView.as_view()),
    path('list/', OrderListView.as_view()),
    path('advertizing/', AdvertisingListView.as_view()),
    path('wallets/', WalletListing.as_view()),
    path('wallets/<int:pk>/request-paid/', WalletChangeStatusToPaidRequest.as_view())
]
