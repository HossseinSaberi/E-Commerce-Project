from rest_framework.test import APITestCase
from django.urls import reverse
from Users.models import Customer , Supplier
from django_fakeredis import FakeRedis
from initial_DataBase import REDIS_OTP_PORT, REDIS_OTP_HOST
import fakeredis , redis

# Create your tests here.
redis_client = redis.Redis(host=REDIS_OTP_HOST, port=REDIS_OTP_PORT)
class TestOTPCode(APITestCase):
    def setUp(self):
        self.customer = Customer(username='test' , password='1234' , email='test@test.com' , mobile_number = '09111111111' , is_mobile_submitted=False)
        self.customer.save()


    # @FakeRedis('account.api_views.redis_client' , )
    def test_generate_activation_code(self):
        url = reverse('GenerateActivationCode')
        body = {
            'mobile_number':'09111111111'
        }
        resp = self.client.post(url , data = body)
        code = redis_client.get('active_code_09111111111').decode()

        self.assertEqual(resp.status_code , 200)
        self.assertEqual(len(code) , 5)


    def test_submit_activation_code(self):
        url = reverse('SubmitActivationCode')
        mobile = '09111111111'
        code = redis_client.get('active_code_09111111111').decode()

        body = {
            'mobile_number' : mobile , 
            'code': code
        }

        resp = self.client.post(url , data=body)

        person_new = Customer.active.get(mobile_number = '09111111111')
        self.assertEqual(resp.status_code , 200)
        self.assertEqual(person_new.is_mobile_submitted , True)


    def test_generate_login_code(self):
        url = reverse('OneTimePasswordLoginCodeGeneration')
        body = {
            'mobile_number':'09111111111'
        }
        resp = self.client.post(url , data = body)
        self.assertEqual(resp.status_code , 404)

        self.customer.is_active = True
        self.customer.save()
        resp = self.client.post(url , data = body)
        code = redis_client.get('09111111111').decode()

        self.assertEqual(resp.status_code , 200)
        self.assertEqual(len(code) , 5)