from django.contrib import admin
from .models import Client, Master, Service, Appointment

class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'name', 'phone', 'login', 'password')  # Поля, отображаемые в списке
    search_fields = ('name', 'phone', 'login')  # Поля, по которым можно искать
    list_filter = ('name',)  # Фильтры справа
    fieldsets = (
        ('Основная информация', {'fields': ['client_id', 'name', 'phone', 'login', 'password']}),
    )

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:  # Если пароль был изменён
            obj.set_password(form.cleaned_data['password'])  # Хэшируем пароль
        super().save_model(request, obj, form, change)

class MasterAdmin(admin.ModelAdmin):
    list_display = ('master_id', 'full_name', 'phone', 'qualification', 'age', 'login', 'password')
    search_fields = ('full_name', 'phone', 'qualification')
    list_filter = ('qualification',)
    fieldsets = (
        ('Основная информация', {'fields': ['master_id', 'full_name', 'phone', 'qualification', 'age', 'login', 'password']}),
    )

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:  # Если пароль был изменён
            obj.set_password(form.cleaned_data['password'])  # Хэшируем пароль
        super().save_model(request, obj, form, change)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_id', 'info', 'price')
    search_fields = ('info',)
    list_filter = ('price',)
    fieldsets = (
        ('Информация об услуге', {'fields': ['service_id', 'info', 'price']}),
    )

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'client', 'date', 'time', 'service', 'master', 'status')
    search_fields = ('client__name', 'master__full_name', 'service__info')
    list_filter = ('status', 'date')
    fieldsets = (
        ('Основная информация', {'fields': ['appointment_id', 'client', 'date', 'time', 'service', 'master', 'status']}),
    )

# Регистрация моделей в админке
admin.site.register(Client, ClientAdmin)
admin.site.register(Master, MasterAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Appointment, AppointmentAdmin)