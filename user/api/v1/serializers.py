from user.models import User
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField


class PhoneNumberSerializer(serializers.Serializer):
    """
    serializer for User PhoneNumber
    """

    PhoneNumber = PhoneNumberField()
    gender = serializers.ChoiceField(
        choices=[
            ('M', 'مذکر'),
            ('F', 'مونث'),
        ]
    )

class OTPSerializer(serializers.Serializer):
    """
    for get the otp code
    """
    
    PhoneNumber = PhoneNumberField()
    otp = serializers.CharField(max_length=255, min_length=4, trim_whitespace=True)
    

class CustomTokenSerializer(serializers.Serializer):
    """
    for verify the token 
    """

    token = serializers.CharField(max_length=255, min_length=4, trim_whitespace=True)


