from django.shortcuts import render
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
# Create your views here.

def home(request):
    return render(request, 'registration/home.html', {})

def register(request):
    if request.method == 'POST':
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        firstname = request.POST.get("firstname", "")
        lastname = request.POST.get("lastname", "")

        #test is user has already registered
        current_users_with_username = User.objects.filter(email=email)
        if len(current_users_with_username) > 0:
            return render(request, 'registration/success.html', {'message': 'You have already registered!'})
        else:
            try:
                validate_email(email)
            except ValidationError as e:
                return render(request, 'registration/success.html', {'message': 'Invalid email address!'})
            u = User(username=email, password=password, email=email, first_name=firstname, last_name=lastname)
            u.save()
            return render(request, 'registration/success.html', {'message': 'Successfully created user!'})
        #ajax registration
    else:
        #non ajax registration
        return render(request, 'registration/register.html', {})

def login(request):
    if request.method == 'POST':
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        user = authenticate(username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return render(request, 'registration/success.html', {'message': 'You are now logged in.'})
        else:
            return render(request, 'registration/success.html', {'message': 'No user! You need to register!'})
    else:
        #non ajax registration
        return render(request, 'registration/login.html', {});

def logout(request):
    auth_logout(request)
    return render(request, 'registration/success.html', {'message': 'Logged out!'})


