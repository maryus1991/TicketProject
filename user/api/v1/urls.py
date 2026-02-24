from django.urls import path
from .views import AuthViewLogin, ChangePasswordAuthenticatedUser, AuthViewValidate, AuthViewVerify, UpdateUserInformations, GetAuthenticatedUserInformations, UpdateUserPhoneNumber


app_name = 'users_api'

urlpatterns = [
    path('auth/login/', AuthViewLogin.as_view(), name='auth-view-login'),
    path('auth/user/', GetAuthenticatedUserInformations.as_view(), name='auth-user_infos'),
    path('auth/password/', ChangePasswordAuthenticatedUser.as_view(), name='auth-user-set-password'),
    path('auth/validate/', AuthViewValidate.as_view(), name='auth-view-login'),
    path('auth/verify/', AuthViewVerify.as_view(), name='auth-view-login'),
    path('auth/update/', UpdateUserInformations.as_view(), name='auth-view-update'),
    path('auth/update/phone-number', UpdateUserPhoneNumber.as_view(), name='auth-view-update-phone-number'),
]
