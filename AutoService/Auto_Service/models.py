from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Client(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    login = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class Master(models.Model):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    experience = models.DecimalField(max_digits=100, decimal_places=0)
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.full_name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class Service(models.Model):
    info = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    masters = models.CharField(max_length=200)

    def __str__(self):
        return self.info

class Appointment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='appointments')
    date = models.CharField(max_length=10)
    time = models.CharField(max_length=5)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='appointments')
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.client.name} - {self.service.info} on {self.date} at {self.time}"