from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from Auto_Service.views import *


router = DefaultRouter()
#router.register(r'clients', ClientViewSet)
router.register(r'masters', MasterViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'appointments', AppointmentViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/client/register/', ClientRegisterView.as_view(), name='client-register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/user/my_appointments/', MyAppointmentsView.as_view(), name='appointments'),
    path('api/user/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/user/logout/', LogoutView.as_view(), name='logout'),
    path('api/all_services/', ServiceListView.as_view(), name='services'),
    path('api/appointments/create/', ClientAppointmentCreateView.as_view(), name='create-appointment'),




# HTML

    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('my_appointments/', appointments_view, name='appointments'),
    path('appointments/create/', appointment_create_view, name='create_appointment'),
    path('change-password/', change_password_view, name='change_password'),
    path('services/', services_view, name='services'),
    path('logout/', logout_view, name='logout'),


#admin
    path('admin-panel/', include('Auto_Service.admin_urls')),
]
