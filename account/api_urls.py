from django.contrib import admin
from django.urls import path, include , re_path
from django.conf import settings
from django.conf.urls.static import static
from .api_views import  GenerateActivationCode , SubmitActivationCode , OneTimePasswordLoginCodeGeneration

urlpatterns = [
    path('GenerateActivationCode/' , GenerateActivationCode.as_view() , name='GenerateActivationCode'),
    path('SubmitActivationCode/' , SubmitActivationCode.as_view() , name='SubmitActivationCode'),
    path('GenerateLoginCode/' , OneTimePasswordLoginCodeGeneration.as_view() , name='OneTimePasswordLoginCodeGeneration'),
]
