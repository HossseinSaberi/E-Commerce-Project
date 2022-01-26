from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from Users.models import Customer
from initial_DataBase import REDIS_OTP_PORT, REDIS_OTP_HOST , SECURITY_CODE , API_KEY
from .utils import check_activate
from .serializers import PhoneSerializer, ActivateAccountSerializer
from rest_framework.parsers import MultiPartParser
import redis
import random
from aiohttp import ClientSession
import asyncio

redis_client = redis.Redis(host=REDIS_OTP_HOST, port=REDIS_OTP_PORT)

class GenerateActivationCode(generics.CreateAPIView):
    model = Customer
    queryset = Customer.objects.all()
    serializer_class = PhoneSerializer
    parser_classes = [MultiPartParser]

    def generate_code(self):
        code = random.randint(10000, 100000)
        return code

    def save_code(self):
        my_code = self.generate_code()
        my_user = "active_code_"+self.request.data['mobile_number']
        redis_client.set(my_user, my_code, ex=600)
        return my_code

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        loop = asyncio.new_event_loop()
        code = self.save_code()
        loop.run_until_complete(send_otp(serializer.data['mobile_number'], code))# if false -- > try again
        return Response({'Success': 'The Code Generate and Send to your mobile Successfuly'}, status=status.HTTP_200_OK)


class SubmitActivationCode(generics.CreateAPIView):
    model = Customer
    queryset = Customer.objects.all()
    serializer_class = ActivateAccountSerializer
    parser_classes = [MultiPartParser]

    def get_code(self):
        code = redis_client.get("active_code_"+self.request.data['mobile_number']).decode()
        return code

    def check_code(self):
        code = self.get_code()
        if code == self.request.data['code']:
            return True
        return False

    def get_user(self):
        try:
            user = Customer.objects.get(mobile_number = self.request.data['mobile_number'])
            return user
        except:
            return None

    def post(self, request, *args, **kwargs):
        if self.check_code():
            user = self.get_user()
            if user :
                user.is_mobile_submitted = True
                user.save()
                return Response({'Success': 'The Account Activate Successfuly'}, status=status.HTTP_200_OK)
            else:
                return Response({'Error': 'User Not Found!'}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({'Error': 'The Code is Wrong'}, status=status.HTTP_400_BAD_REQUEST)



class OneTimePasswordLoginCodeGeneration(GenerateActivationCode):

    def check_user_activation(self,user):
        if user.is_mobile_submitted == True :
            return user
        else :
            return None

    def check_user(self):
        user = Customer.objects.get(mobile_number = self.request.data['mobile_number'])
        check_activate = self.check_user_activation(user)
        if user :
            if check_activate:
                return True
        return False
    
    def save_code(self):
        if self.check_user():
                
            my_code = self.generate_code()
            my_user = self.request.data['mobile_number']
            redis_client.set(my_user, my_code, ex=600)
            return my_code
        
        else:
            return None

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        loop = asyncio.new_event_loop()
        code = self.save_code()
        if code == None:
            return Response({'Error' : 'The active user with this phone number not found'} , status=status.HTTP_404_NOT_FOUND)
        loop.run_until_complete(send_otp(serializer.data['mobile_number'], code))# if false -- > try again
        return Response({'Success': 'The Code Generate and Send to your mobile Successfuly'}, status=status.HTTP_200_OK)


    
        

async def send_otp(phone, otp):
    async with ClientSession() as session:
        unit_url = "https://RestfulSms.com/api/Token"
        validation_headers = {'content-type': 'application/json'}
        validation_body = {"SecretKey": SECURITY_CODE, "UserApiKey": API_KEY}
        response = await session.post(unit_url, json=validation_body, headers=validation_headers)
        if response.status != 201: #404
            return False
        data1 = await response.json()
        sending_sms_url = "http://RestfulSms.com/api/VerificationCode"
        sms_body = {"Code": otp, "MobileNumber": phone}
        headers_sms = {'content-type': 'application/json',
                        "x-sms-ir-secure-token": data1["TokenKey"]}
        response = await session.post(sending_sms_url, json=sms_body, headers=headers_sms)
        if response.status != 201:
            return False
        return await response.json()