from django.contrib.auth.hashers import check_password
from .models import Client, Master

class ClientAuthBackend:
    def authenticate(self, request, login=None, password=None):
        try:
            client = Client.objects.get(login=login)
            if check_password(password, client.password):
                return client
        except Client.DoesNotExist:
            return None

class MasterAuthBackend:
    def authenticate(self, request, login=None, password=None):
        try:
            master = Master.objects.get(login=login)
            if check_password(password, master.password):
                return master
        except Master.DoesNotExist:
            return None