from rest_framework import viewsets, generics, permissions
from .models import Client, Master, Service, Appointment
from .serializers import ClientSerializer, MasterSerializer, ServiceSerializer, AppointmentSerializer, ClientRegisterSerializer, MasterRegisterSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class MasterViewSet(viewsets.ModelViewSet):
    queryset = Master.objects.all()
    serializer_class = MasterSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class ClientRegisterView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientRegisterSerializer

class MasterRegisterView(generics.CreateAPIView):
    queryset = Master.objects.all()
    serializer_class = MasterRegisterSerializer