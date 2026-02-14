

from config import settings
 
from kavenegar import KavenegarAPI

def send_otp(number, otp):
    try:
        api = KavenegarAPI(settings.KAVEH_NEGAR_OTP)
        params = { 
            'receptor': number,
            'template': 'main',
            'token': str(otp),
            'type': 'sms',
        }
        response = api.verify_lookup(params)
        print(response.json())
    except Exception as e:
        print(e)


 