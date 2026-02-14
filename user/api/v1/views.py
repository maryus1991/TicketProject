from rest_framework.generics import GenericAPIView
from user.models import User
from rest_framework import status, response
from .serializers import PhoneNumberSerializer, OTPSerializer, CustomTokenSerializer
from django.utils.crypto import get_random_string
from django.db.transaction import atomic
from rest_framework.authtoken.models import Token


class AuthViewLogin(GenericAPIView):
    '''
    get PhoneNumber and create user if not exists and send otp code for login
    201 for success
    400 other errors
    '''
    serializer_class = PhoneNumberSerializer

    def post(self, request, *args, **kwargs):



        data = PhoneNumberSerializer(data=request.data)
        try:
            data.is_valid(raise_exception=True)
            PhoneNumber = data.validated_data.get('PhoneNumber')
            with atomic():
                user, created = User.objects.get_or_create(
                    PhoneNumber=PhoneNumber
                )

                
                if created:
                    if data.validated_data.get('gender'):
                        user.gender = data.validated_data.get('gender')
                    else:
                        raise 'the gender of user should send'


                    password = get_random_string(8)
                    user.set_password(password)

                user.save()

                user.set_otp()
                
                return response.Response('set user successfully and otp has been send', status=status.HTTP_201_CREATED)

        except Exception as error :
            error = f"' {error} ' has been rise in AuthView for User : {PhoneNumber} That for create or login "
            print(error)
            # todo: add logger
            return response.Response(error, status=status.HTTP_400_BAD_REQUEST)


class AuthViewVerify(GenericAPIView):
    """
    get the otp code and phone number and return the auth token

    200 for success
    403 for wrong and expire code
    400 for other errors
    
    """
    serializer_class = OTPSerializer

    def put(self, request, *args, **kwargs):


        data = OTPSerializer(data=request.data)

        try:
            data.is_valid(raise_exception=True)
            PhoneNumber = data.validated_data.get('PhoneNumber')
            otp = data.validated_data.get('otp')

            with atomic():
                user:User = User.objects.filter(
                    PhoneNumber=PhoneNumber
                )

                if not user.exists or user.count() != 1 :
                    return response.Response('user not exists', status=status.HTTP_401_UNAUTHORIZED)
                
                else:
                    user = user.last()

                result = user.verify_otp(otp)

                if result[0] == 200:
                    return response.Response({'token': result[1]}, status=status.HTTP_200_OK)
                else :
                    return response.Response(result[1], status=status.HTTP_403_FORBIDDEN)

        except Exception as error :
            error = f"' {error} ' has been rise in AuthView for User : {PhoneNumber} That for verify the user"
            print(error)
            # todo: add logger
            return response.Response(error, status=status.HTTP_400_BAD_REQUEST)
        

class AuthViewValidate(GenericAPIView):
    """
    check the token
    
    204 for valid token
    401 for not valid token
    400 for other errors

    """

    serializer_class = CustomTokenSerializer 

    def patch(self, request, *args, **kwargs):

        data = CustomTokenSerializer(data=request.data)

        try:
            data.is_valid(raise_exception=True)
            token: Token = data.validated_data.get('token')
            
            with atomic():
                token = Token.objects.filter(key=token)

                if token.exists():
                    return response.Response('the tokne is valid!', status=status.HTTP_204_NO_CONTENT)
                else:
                    return response.Response('the tokne is not valid!', status=status.HTTP_401_UNAUTHORIZED)

        except Exception as error :
            error = f"' {error} ' has been rise in AuthView that for validate the token "
            print(error)
            # todo: add logger
            return response.Response(error, status=status.HTTP_400_BAD_REQUEST)


    