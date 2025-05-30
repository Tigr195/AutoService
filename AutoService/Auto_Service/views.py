from datetime import datetime, timezone, timedelta

from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError

from .models import Client, Master, Service, Appointment
from .permissions import IsClient, IsMaster
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth.models import User


def check_and_refresh_token(request):
    access_token = request.session.get('access_token')
    refresh_token = request.session.get('refresh_token')

    if not access_token or not refresh_token:
        logout(request)
        return False
    try:
        access = AccessToken(access_token)
        if access['exp'] < datetime.now(timezone.utc).timestamp():
            raise TokenError("Access token expired")
        return True
    except TokenError:
        try:
            refresh = RefreshToken(refresh_token)
            new_access = refresh.access_token
            request.session['access_token'] = str(new_access)
            return True
        except TokenError:
            logout(request)
            return False

def generate_time_slots(start='09:00', end='18:00', step_minutes=30):
    slots = []
    current_dt = datetime.combine(date.today(), datetime.strptime(start, "%H:%M").time())
    end_dt = datetime.combine(date.today(), datetime.strptime(end, "%H:%M").time())

    while current_dt <= end_dt:
        slots.append(current_dt.time())
        current_dt += timedelta(minutes=step_minutes)

    return slots

# class ClientViewSet(viewsets.ModelViewSet):
#     queryset = Client.objects.all()
#     serializer_class = ClientRegisterSerializer

class MasterViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Master.objects.all()
    serializer_class = MasterSerializer

class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class ServiceListView(APIView):

    def get(self, request):
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)


class MyAppointmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if hasattr(user, 'client'):
            appointments = Appointment.objects.filter(client=user.client)
        elif hasattr(user, 'master'):
            appointments = Appointment.objects.filter(master=user.master)
        else:
            return Response({'error': 'Пользователь не является ни клиентом, ни мастером'}, status=403)

        serializer = AppointmentSerializer(appointments.order_by("date", "time"), many=True)
        return Response(serializer.data)

class ClientRegisterView(APIView):
    def post(self, request):
        serializer = ClientRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Клиент зарегистрирован'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        login = request.data.get('login')
        password = request.data.get('password')

        user = authenticate(request, username=login, password=password)
        if user is None:
            return Response({'error': 'Неверный логин или пароль'}, status=401)

        if user.is_client:
            user_type = 'client'
        elif user.is_master:
            user_type = 'master'
        else:
            user_type = 'unknown'

        refresh = RefreshToken.for_user(user)
        refresh['user_type'] = user_type

        access = refresh.access_token

        return Response({
            'refresh': str(refresh),
            'access': str(access),
            'user_type': user_type
        }, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response({"detail": "Неверный текущий пароль"}, status=status.HTTP_400_BAD_REQUEST)

        if not new_password:
            return Response({"detail": "Новый пароль не может быть пустым"}, status=status.HTTP_400_BAD_REQUEST)

        if old_password == new_password:
            return Response({"detail": "Новый пароль не должен совпадать с текущим"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response({"detail": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"detail": "Пароль успешно изменён"})

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Вы успешно вышли из системы"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"detail": "Ошибка отзыва токена"}, status=status.HTTP_400_BAD_REQUEST)

class ClientAppointmentCreateView(APIView):
    permission_classes = [IsAuthenticated, IsClient]

    def post(self, request):
        serializer = AppointmentCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Запись успешно создана'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#  HTML


@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        login_ = request.POST.get('login')
        password = request.POST.get('password')

        if User.objects.filter(username=login_).exists():
            return render(request, 'register.html', {'error': 'Логин уже занят'})

        user = User.objects.create_user(
            username=login_,
            password=password,
        )
        user.is_client = True
        user.save()

        Client.objects.create(
            user=user,
            name=name,
            phone=phone
        )
        return redirect('login')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        login_ = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(request, username=login_, password=password)
        if user is not None:
            login(request, user)

            refresh = RefreshToken.for_user(user)
            request.session['access_token'] = str(refresh.access_token)
            request.session['refresh_token'] = str(refresh)

            if user.is_superuser or user.is_staff:
                return redirect('admin_dashboard')
            return redirect('services')
        else:
            return render(request, 'login.html', {'error': 'Неверный логин или пароль'})
    return render(request, 'login.html')


@login_required
def appointments_view(request):
    if not check_and_refresh_token(request):
        return redirect('login')
    user = request.user

    if hasattr(user, 'client'):
        appointments = Appointment.objects.filter(client=user.client).order_by("date", "time")
    elif hasattr(user, 'master'):
        appointments = Appointment.objects.filter(master=user.master).order_by("date", "time")
    else:
        appointments = []

    return render(request, 'appointments.html', {'appointments': appointments})


@login_required
def appointment_create_view(request):
    if not hasattr(request.user, 'client'):
        return redirect('appointments')

    services = Service.objects.all()
    masters = Master.objects.all()
    time_slots = None
    errors = None
    selected_date = ''
    selected_master = ''

    if request.method == 'GET':
        selected_date = request.GET.get('date')
        selected_master = request.GET.get('master')

        if selected_date and selected_master:
            try:
                date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()

                if date_obj < date.today():
                    errors = {'date': ['Нельзя выбрать прошедшую дату.']}
                else:
                    master = Master.objects.get(id=selected_master)

                    all_slots = generate_time_slots()
                    busy_slots = Appointment.objects.filter(
                        date=date_obj,
                        master=master
                    ).values_list('time', flat=True)

                    time_slots = [slot for slot in all_slots if slot not in busy_slots]
            except (ValueError, Master.DoesNotExist):
                time_slots = []

    elif request.method == 'POST':
        selected_date = request.POST.get('date', '')
        selected_master = request.POST.get('master', '')

        serializer = AppointmentCreateSerializer(data=request.POST, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return redirect('appointments')
        else:
            errors = serializer.errors

    return render(request, 'appointment_create.html', {
        'services': services,
        'masters': masters,
        'time_slots': time_slots,
        'errors': errors,
        'selected_date': selected_date,
        'selected_master': selected_master,
    })

@login_required
def change_password_view(request):
    if not check_and_refresh_token(request):
        return redirect('login')
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        user = request.user

        if not user.check_password(old_password):
            return render(request, 'change_password.html', {'error': 'Неверный текущий пароль'})

        if old_password == new_password:
            return render(request, 'change_password.html', {'error': 'Новый пароль не должен совпадать с текущим'})

        # try:
        #     validate_password(new_password, user)
        # except ValidationError as e:
        #     return render(request, 'change_password.html', {'error': e.messages})

        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request, user)

        return render(request, 'change_password.html', {'success': 'Пароль успешно изменён'})

    return render(request, 'change_password.html')

def services_view(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})

@login_required
def logout_view(request):
    request.session.flush()
    return redirect('login')
