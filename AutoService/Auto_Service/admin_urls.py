from django.urls import path
from . import admin_views

urlpatterns = [
    path('', admin_views.admin_dashboard, name='admin_dashboard'),

    # Услуги
    path('services/', admin_views.admin_services_view, name='admin_services'),
    path('services/add/', admin_views.add_service_view, name='add_service'),

    # Мастера
    path('masters/', admin_views.admin_masters_view, name='admin_masters'),
    path('masters/add/', admin_views.add_master_view, name='add_master'),

    # Клиенты
    path('clients/', admin_views.admin_clients_view, name='admin_clients'),

    # Записи
    path('appointments/', admin_views.admin_appointments_view, name='admin_appointments'),
    path('appointments/<int:appointment_id>/change-status/', admin_views.edit_appointment_status, name='edit_appointment'),
]
