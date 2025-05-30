from datetime import time, date, datetime

from rest_framework import serializers, request
from .models import Client, Master, Service, Appointment
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['login', 'password', 'is_client', 'is_master']

class ClientRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Client
        fields = ['username', 'password', 'name', 'phone']

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        user = User.objects.create_user(username=username, password=password)
        client = Client.objects.create(user=user, **validated_data)
        return client

class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name', read_only=True)
    master_name = serializers.CharField(source='master.full_name', read_only=True)
    service_info = serializers.CharField(source='service.info', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'client', 'client_name',
            'master', 'master_name',
            'service_info',
            'date', 'time', 'status'
        ]

class AppointmentCreateSerializer(serializers.ModelSerializer):
    time = serializers.TimeField(format='%H:%M', input_formats=['%H:%M', '%H:%M:%S'])

    class Meta:
        model = Appointment
        fields = ['date', 'time', 'service', 'master']

    def validate(self, data):
        selected_date = data['date']
        selected_time = data['time']
        master = data['master']

        selected_date_str = "2025-05-30"
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        if selected_date < date.today():
            raise serializers.ValidationError({'date': 'Дата не может быть в прошлом.'})




        exists = Appointment.objects.filter(
            master=master,
            date=selected_date,
            time=selected_time
        ).exists()
        if exists:
            raise serializers.ValidationError({'time': 'Мастер уже занят на это время.'})

        return data


    def create(self, validated_data):
        return Appointment.objects.create(client=self.context['request'].user.client, **validated_data)
