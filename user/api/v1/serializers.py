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

class PhoneNumberSerializer2(serializers.Serializer):
    """
    serializer for User PhoneNumber
    """

    PhoneNumber = PhoneNumberField()

class UserInformationSerializer(serializers.ModelSerializer):

    ''' 
    for edit user infos
    '''

    class Meta:
        model = User
        fields = [
           
            "first_name",
            "last_name",
            "gender",
            'email'

        ]

class UserAllInformationSerializer(serializers.ModelSerializer):

    ''' 
      user infos
    '''

    class Meta:
        model = User
        read_only_fields = ['__all__']
        exclude = ['password', 'user_permissions', 'groups', 'otp_expiry_date', 'otp']


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

class PasswordSerializer(serializers.Serializer):
    """
    for verify the token 
    """

    password = serializers.CharField(max_length=255, min_length=4, trim_whitespace=True)


