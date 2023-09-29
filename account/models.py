from django.db import models


# Create your models here.


class Client(models.Model):
    name = models.TextField()
    surname = models.TextField()
    email = models.EmailField()
    password = models.TextField(max_length=255)
    is_active = models.BooleanField(default=False)


class Account(models.Model):
    date_created = models.DateField()
    balance = models.FloatField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
