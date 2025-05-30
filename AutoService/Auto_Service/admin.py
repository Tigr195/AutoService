from django.contrib import admin
from .models import Client, Master, Service, Appointment
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class MasterInline(admin.StackedInline):
    model = Master
    can_delete = False
    verbose_name_plural = 'Master'

class UserAdmin(BaseUserAdmin):
    inlines = [MasterInline]

    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('username',)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'get_username')
    search_fields = ('name', 'phone', 'user__username')
    list_filter = ('name',)

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Login'

class MasterAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'experience', 'get_username')
    search_fields = ('full_name', 'phone', 'experience', 'user__username')

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Login'

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'info', 'price')
    search_fields = ('info',)
    list_filter = ('price',)
    fieldsets = (
        ('Информация об услуге', {'fields': ['info', 'price']}),
    )

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'date', 'time', 'service', 'master', 'status')
    search_fields = ('client__name', 'master__full_name', 'service__info')
    list_filter = ('status', 'date')
    fieldsets = (
        ('Основная информация', {'fields': ['client', 'date', 'time', 'service', 'master', 'status']}),
    )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Master, MasterAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Appointment, AppointmentAdmin)