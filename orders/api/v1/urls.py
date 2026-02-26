from django.urls import path
from .views import( SetOrderPostView,
                    AdvertisingListView,
                    WalletListing, 
                    WalletChangeStatusToPaidRequest, 
                    OrderListView, 
                    SalonOrdersList,
                    UserCancelOrderBeforPayment,
                    UserCancelOrderAfterPayment
)
urlpatterns = [
    path('create/', SetOrderPostView.as_view()),
    path('list/', OrderListView.as_view()),
    path('advertizing/', AdvertisingListView.as_view()),
    path('wallets/', WalletListing.as_view()),
    path('wallets/<int:pk>/request-paid/', WalletChangeStatusToPaidRequest.as_view()),
    path('salon/', SalonOrdersList.as_view()),
    path('cancelling/<int:pk>/befor-payment/', UserCancelOrderBeforPayment.as_view()),
    path('cancelling/<int:pk>/after-payment/', UserCancelOrderAfterPayment.as_view()),
]
