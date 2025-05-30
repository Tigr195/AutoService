from django import forms
from .models import Service, Appointment

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['info', 'price']

class AppointmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['status']
