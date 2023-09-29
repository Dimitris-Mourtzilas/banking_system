import logging

from datetime import date
from django.core.exceptions import ObjectDoesNotExist

from account import models
from account.models import Client, Account

logger = logging.getLogger(__name__)

from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        client = Client(name=name, surname=surname, email=email, password=password)
        client.save()
        return render(request, 'index.html', {'success_message': 'User registered succesfully'})
    return render(request, 'register.html')


def authenticate(request):
    try:
        user = models.Client.objects.get(email=request.POST.get('email'), password=request.POST.get('password'))
        user.is_active = True
        user.save()
        return redirect('dashboard')
    except ObjectDoesNotExist:
        return render('index.html', {'error_message': 'User does not exist'})


def dashboard(request):
    return render(request, 'user/dashboard.html')


def account_creation(request):

    return render(request,'user/account_creation.html')


def add_account(request):

    if request.method == "POST":
        balance = request.POST.get('balance')
        client_id = Client.objects.filter(is_active=True).values()
        print(client_id[0]['id'])
        account = Account(date_created=date.today(),balance=balance,client_id=client_id[0]['id'])
        account.save()
        return render(request,'user/dashboard.html',{'account_success':'Created new account'})
