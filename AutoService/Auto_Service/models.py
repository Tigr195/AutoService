from django.db import models


class Client(models.Model):
    client_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Master(models.Model):
    master_id = models.CharField(max_length=100, primary_key=True)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    qualification = models.CharField(max_length=100)
    age = models.CharField(max_length=3)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    video = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name

class Service(models.Model):
    service_id = models.CharField(max_length=100, primary_key=True)
    info = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    masters = models.CharField(max_length=200)

    def __str__(self):
        return self.info

class Appointment(models.Model):
    appointment_id = models.CharField(max_length=100, primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='appointments')
    date = models.CharField(max_length=10)
    time = models.CharField(max_length=5)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='appointments')
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.client.name} - {self.service.info} on {self.date} at {self.time}"