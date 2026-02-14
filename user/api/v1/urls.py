from django.urls import path
from .views import AuthViewLogin, AuthViewValidate, AuthViewVerify


app_name = 'users_api'

urlpatterns = [
    path('auth/login/', AuthViewLogin.as_view(), name='auth-view-login'),
    path('auth/validate/', AuthViewValidate.as_view(), name='auth-view-login'),
    path('auth/verify/', AuthViewVerify.as_view(), name='auth-view-login'),
]
