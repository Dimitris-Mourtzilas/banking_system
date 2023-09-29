import logging

from django.core.exceptions import ObjectDoesNotExist

from account import models
from account.models import Client

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
        client = Client(name=name,surname=surname,email=email,password=password)
        client.save()
        return render(request,'index.html',{'success_message':'User registered succesfully'})
    return render(request, 'register.html')


def authenticate(request):
    try:
        user = models.Client.objects.get(email = request.POST.get('email'),password=request.POST.get('password'))
        return render('user/dashboard.html',{'username':user.__getattribute__('name')})
    except ObjectDoesNotExist:
        return render('index.html',{'error_message':'User does not exist'})
