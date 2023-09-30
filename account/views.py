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
    print(Client.objects.filter(is_active=True).values()[0]['id'])
    accounts = Account.objects.select_related('client').filter(client__is_active=True)
    return render(request, 'user/dashboard.html', {'accounts': accounts})


def create_an_account(request):
    return render(request, 'user/account_creation.html', {'date': date.today()})


def validate_account(request):
    user = Client.objects.filter(is_active=True).values()
    balance = request.POST.get('balance')
    date_created = request.POST.get('date_created')
    account = Account(date_created=date_created, balance=balance, client_id=user[0]['id'])
    account.save()
    return render(request, 'user/dashboard.html',
                  {'acc_message': 'Successfully created account', 'accounts': Account.objects.select_related('client').filter(client__is_active=True)})


def logout(request):
    cl = Client.objects.get(is_active=True)
    cl.is_active = False
    cl.save()
    return redirect('index')

def edit_account(request):

    return render(request,'user/edit_account.html')




def validate_edit(request):
        account = Account.objects.get('id',request.POST.get('id'))
        print(account)