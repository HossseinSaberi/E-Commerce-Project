from aiohttp import request
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, logout, get_user_model, login
from django.contrib.auth import get_user_model
from .forms import LoginForm, SignInForm, MobileActivateForm, SubmittedCodeForm
from django.contrib import messages
from Users.models import Supplier, Customer
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, UpdateView, CreateView , TemplateView
from .api_views import send_otp
import random
import redis
import asyncio

from initial_DataBase import REDIS_OTP_HOST, REDIS_OTP_PORT


redis_client = redis.Redis(host=REDIS_OTP_HOST, port=REDIS_OTP_PORT)
CreateUser = get_user_model()


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            try:
                get_user = Customer.suppliers.filter(Q(username=username) | Q(
                    email=username) | Q(mobile_number=username))
            except:
                get_user = None

            if get_user:
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(
                    request, f"Dear {username} , Welcome Back To Your Dashboard !", extra_tags='success')

                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect(reverse('Usersindex'), {'request': request})
            else:
                messages.error(
                    request, f"You have no account as a supplier yet !", extra_tags='warning')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def mobile_log_in(request):
    if request.method == 'POST':
        form = MobileActivateForm(request.POST)
        if form.is_valid():
            username = request.POST['mobile_number']
            '''use login def for continue'''


def sign_in(request):

    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            email = form.cleaned_data.get('Email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            mobile = form.cleaned_data.get('mobile_number')
            sign_in_user = CreateUser(
                username=username, email=email, is_supplier=True, mobile_number=mobile)
            new_supplier = Supplier(
                customer=sign_in_user, supplier_blog=username+'_Blog ')
            sign_in_user.set_password(password)
            sign_in_user.save()
            new_supplier.save()
            print(sign_in_user)
            messages.success(
                request, "You're Registering was Success", extra_tags='success')
            return redirect(reverse('log_in'))
    else:
        form = SignInForm()
    return render(request, 'registration/signin.html', {'form': form})


def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


class Activate(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = SubmittedCodeForm
    template_name = 'registration/submittCode.html'
    success_url = 'usersPosts'

    def get_queryset(self):
        return super().get_queryset().get(mobile_number=self.request.user.mobile_number)

    def get_object(self):
        queryset = self.get_queryset()
        return queryset

    def generate_code(self):
        code = random.randint(10000, 100000)
        return code

    def save_code(self):
        my_code = self.generate_code()
        my_user = "active_code_"+self.request.user.mobile_number
        redis_client.set(my_user, my_code, ex=600)
        return my_code

    def send_sms(self):
        loop = asyncio.new_event_loop()
        code = self.save_code()
        loop.run_until_complete(
            send_otp(self.request.user.mobile_number, code))

    def get(self, request, *args, **kwargs):
        self.send_sms()
        return super().get(request, *args, **kwargs)

    def check_active_code(self, code):
        entire_code = redis_client.get("active_code_"+self.request.user.mobile_number).decode()
        if code == entire_code:
            return True
        return False

    def form_valid(self, form):
        user = self.get_object()
        code = self.request.POST['code']
        if self.check_active_code(code):
            user.is_mobile_submitted = True
            user.save()
        else:
            messages.error(self.request, "You're Submitted Code Is Wrong", extra_tags='danger')
        return redirect(reverse('Usersindex'))

    def post(self, request, *args: str, **kwargs):
        return super().post(request, *args, **kwargs)
