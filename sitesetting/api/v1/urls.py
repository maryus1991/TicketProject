from django.urls import path
from .views import ContactView, SiteView, TeamView


urlpatterns = [
    path('site/', SiteView.as_view()),
    path('team/', TeamView.as_view()),
    path('contact/', ContactView.as_view())
]
