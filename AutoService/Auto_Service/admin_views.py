from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Service, Master, Client, Appointment
from .forms import ServiceForm, AppointmentUpdateForm

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin_panel/dashboard.html')

@user_passes_test(is_admin)
def admin_services_view(request):
    services = Service.objects.all()
    return render(request, 'admin_panel/admin_services.html', {'services': services})

@user_passes_test(is_admin)
def admin_masters_view(request):
    masters = Master.objects.all()
    return render(request, 'admin_panel/admin_masters.html', {'masters': masters})

@user_passes_test(is_admin)
def admin_clients_view(request):
    clients = Client.objects.all()
    return render(request, 'admin_panel/admin_clients.html', {'clients': clients})

@user_passes_test(is_admin)
def admin_appointments_view(request):
    appointments = Appointment.objects.all()
    return render(request, 'admin_panel/admin_appointments.html', {'appointments': appointments})

@user_passes_test(is_admin)
def edit_appointment_status(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = AppointmentUpdateForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('admin_appointments')
    else:
        form = AppointmentUpdateForm(instance=appointment)
    return render(request, 'admin_panel/edit_appointment.html', {'form': form})

@user_passes_test(is_admin)
def add_service_view(request):
    if request.method == 'POST':
        info = request.POST.get('name')
        price = request.POST.get('price')

        if not info or not price:
            return render(request, 'admin_panel/add_service.html', {'error': 'Заполните все поля'})

        Service.objects.create(info=info, price=price)
        return redirect('admin_services')

    return render(request, 'admin_panel/add_service.html')

@user_passes_test(is_admin)
def add_master_view(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        experience = request.POST.get('experience')

        if User.objects.filter(username=login).exists():
            return render(request, 'admin_panel/add_master.html', {'error': 'Логин уже занят'})

        user = User.objects.create_user(
            username=login,
            password=password
        )
        user.is_master = True
        user.save()

        Master.objects.create(
            user=user,
            full_name=full_name,
            phone=phone,
            experience=experience
        )

        return redirect('admin_masters')

    return render(request, 'admin_panel/add_master.html')
