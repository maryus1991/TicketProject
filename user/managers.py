from django.contrib.auth.models import UserManager as DjangoUserManager
from django.core.exceptions import ValidationError
from phonenumber_field.validators import validate_phonenumber
from phonenumber_field.phonenumber import PhoneNumber as PN
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string


def validate_phone_number(number) -> None:
    try:
        validate_phonenumber(number)
    except ValidationError:
        raise ValidationError("Enter a valid phone number")
    

class UserManager(DjangoUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValidationError("Enter a valid phone number")

        if not password:
            password = get_random_string(8)

  
        phone_number = PN.from_string(str(phone_number))
        
        if PN.is_valid(phone_number):
            validate_phone_number(phone_number)
            user = self.model(PhoneNumber=phone_number, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_user(self, PhoneNumber, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", False)
        return self._create_user(PhoneNumber, password **extra_fields)

    def create_staff_user(self, PhoneNumber, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        if extra_fields.get("is_superuser") is not False:
            raise ValueError("Superuser must have is_superuser=False.")
        
        return self._create_user(PhoneNumber, password, **extra_fields)

    def create_superuser(
        self, PhoneNumber, password, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)
 

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_active") is not True:
            raise ValueError(_("Superuser must have is_active=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        
        return self._create_user(PhoneNumber, password, **extra_fields)