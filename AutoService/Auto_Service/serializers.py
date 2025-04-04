from rest_framework import serializers
from .models import Client, Master, Service, Appointment
from django.contrib.auth.hashers import make_password

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class ClientRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['name', 'phone', 'login', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return Client.objects.create(**validated_data)

class MasterRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = ['full_name', 'phone', 'experience', 'login', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return Master.objects.create(**validated_data)