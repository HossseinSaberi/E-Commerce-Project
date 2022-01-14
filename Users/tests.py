from rest_framework.test import APITestCase
from django.urls import reverse

from Users.models import Customer

# Create your tests here.
class TestProfile(APITestCase):
    def setUp(self):
        self.new_profile = Customer.objects.create(username='test' , password = '1234' , email='test@test.com' , mobile_number = '0911111111')

    def test_update_profile(self):
        url = reverse('api_Profile' , kwargs={'pk': self.new_profile.id})
        new_name = "new name"
        body = {
            "id" : self.new_profile.id ,
           "username" : new_name ,
           "password" :"1234",
           "email" : 'test@test.com',
           "mobile_number" : '09111111111'
        }
        resp = self.client.put(url , data= body)
        print(resp.data)
        self.assertEquals(resp.status_code , 200)
        self.assertEquals(resp.data['username'] , "new name")

    def test_get_profile(self):
        url = reverse('api_Profile' , kwargs={'pk': self.new_profile.id})
        resp = self.client.get(url)
        self.assertEquals(resp.status_code , 200)
