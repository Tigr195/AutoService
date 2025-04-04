from django.contrib import admin
from django.urls import path


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Auto_Service.views import ClientViewSet, MasterViewSet, ServiceViewSet, AppointmentViewSet, ClientRegisterView, MasterRegisterView

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'masters', MasterViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'appointments', AppointmentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/register/client/', ClientRegisterView.as_view(), name='client-register'),
    path('api/auth/register/master/', MasterRegisterView.as_view(), name='master-register'),
]
