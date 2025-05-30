from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.db import models

from django.utils.timezone import now


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    last_login = models.DateTimeField(default=now)

    def __str__(self):
        return self.name



class Master(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    experience = models.DecimalField(max_digits=100, decimal_places=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name



class Service(models.Model):
    info = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return self.info

class Appointment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='appointments')
    date = models.CharField(max_length=10)
    time = models.TimeField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='appointments')
    status = models.CharField(max_length=50, default='Запланировано')

    def __str__(self):
        return f"{self.client.name} - {self.service.info} on {self.date} at {self.time}"