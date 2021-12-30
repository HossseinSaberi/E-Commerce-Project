from django.http.response import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth import get_user_model
from .forms import LoginForm, SignInForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from Users.models import Supplier , Customer

CreateUser = get_user_model()


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            print(username)
            print(password)
            try:
                get_user = Customer.objects.get(username=username)
                supplier_user = get_user.supplier
            except:
                supplier_user = None
                
            if supplier_user:
                user = authenticate(username=username, password=password)
                if user:
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

# TODO
# it doesnot work check it
# its problem is after press submit button


def sign_in(request):

    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            email=form.cleaned_data.get('Email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            sign_in_user = CreateUser(username=username,password=password,email=email)
            supplier = Supplier(customer=sign_in_user,supplier_blog=username+' Blog',is_supplier=True)
            sign_in_user.save()
            supplier.save()
            print(sign_in_user)
            login(request, sign_in_user)
            messages.success(
                request, "You're Registering was Success", extra_tags='success')
            return redirect(reverse('log_in'))
    else:
        form = SignInForm()
    return render(request, 'registration/signin.html', {'form': form})


def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
