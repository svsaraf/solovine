from django.shortcuts import render
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from utils.mailgun_email import send_registration_email, send_password_reset
import random
import string
# Create your views here.

def home(request):
    return render(request, 'registration/home.html', {})

def faq(request):
    return render(request, 'registration/faq.html', {})

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
            u = User.objects.create_user(username=email, password=password, email=email, first_name=firstname, last_name=lastname)
            u.save()
            send_registration_email(email)
            user = authenticate(username=email, password=password)
            auth_login(request, user)
            response = render(request, 'registration/success.html', {'message': 'Created user!'})
            response['X-IC-Redirect'] = '/user/' + user.email
            return response
            #return render(request, 'registration/success.html', {'message': 'Successfully created user!'})
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
            #return render(request, 'registration/success.html', {'message': 'You are now logged in.'})
            response = render(request, 'registration/success.html', {'message': 'You are now logged in.'})
            response['X-IC-Redirect'] = '/user/' + user.email
            return response
        else:
            return render(request, 'registration/success.html', {'message': 'No user! You need to register!'})
    else:
        #non ajax registration
        return render(request, 'registration/login.html', {})

def forgot(request):
    if request.method == 'POST':
        # reset password and email it to user
        email = request.POST.get("email", "")
        user = User.objects.get(username=email)
        if user is not None:
            newpw = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            user.set_password(newpw)
            user.save()
            send_password_reset(user.username, newpw)
            return render(request, 'registration/success.html', {'message': 'Password reset! Check your email, it should get there within 5 minutes.'})
        else:
            return render(request, 'registration/success.html', {'message': 'That email isn\'t in our system. Please register.'})
    else:
        return render(request, 'registration/forgot.html', {})

def logout(request):
    auth_logout(request)
    return render(request, 'registration/success.html', {'message': 'Logged out!'})

