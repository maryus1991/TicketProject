from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
 

from .models import User
 

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    for set the user admin options
    """

    model = User
    list_display = ("PhoneNumber", "is_verified", "is_superuser", "is_active")
    list_filter = ("is_verified", "is_superuser", "is_active", "PhoneNumber")
    search_fields = ("PhoneNumber", "first_name", "last_name")
    ordering = ("is_verified", "is_superuser", "is_active", "PhoneNumber")

    add_fieldsets = (
        (
            "Authentication",
            {
                "fields": (
                    "PhoneNumber",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "email",
                    "gender",
                    "type_of_user",
                
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "is_verified",
                )
            },
        ),
        ("Group&Permissions", {"fields": ("groups", "user_permissions")}),
    )

    fieldsets = (
        (
            "Authentication",
            {
                "fields": (
                    "PhoneNumber",
                    "email",
                    "password",
                    "first_name",
                    "last_name",
                    "gender",
                    "otp",
                 
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "is_verified",
                    "type_of_user",
                )
            },
        ),
        ("Group&Permissions", {"fields": ("groups", "user_permissions")}),
        (
            "Important Date",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                    "otp_expiry_date",
                )
            },
        ),
    )