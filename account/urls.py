from django.urls import path
from .views import log_in, log_out , sign_in
urlpatterns = [
    path('/login/' , log_in , name='log_in'),
    path('/signin/' , sign_in , name='sign_in'),
    path('/logout/' , log_out , name='log_out')
]
