import os
from django.core.management.base import BaseCommand
from Auto_Service.models import Client, Master, Service, Appointment

class Command(BaseCommand):
    help = 'Заполняет базу данных данными из текстового файла'

    def handle(self, *args, **kwargs):
        file_path = 'data.txt'  # Путь к файлу с данными
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"Файл {file_path} не найден!"))
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(',')
                entity_type = parts[0]

                if entity_type == 'Client':
                    self.create_client(parts[1:])
                elif entity_type == 'Master':
                    self.create_master(parts[1:])
                elif entity_type == 'Service':
                    self.create_service(parts[1:])
                elif entity_type == 'Appointment':
                    self.create_appointment(parts[1:])
                else:
                    self.stdout.write(self.style.WARNING(f"Неизвестный тип сущности: {entity_type}"))
                    continue
        self.stdout.write(self.style.SUCCESS("База данных успешно заполнена!"))

    def create_client(self, data):
        client_id, name, phone, login, password = data
        client = Client(client_id=client_id, name=name, phone=phone, login=login)
        client.set_password(password)
        client.save()
        self.stdout.write(self.style.SUCCESS(f"Создан клиент: {name}"))

    def create_master(self, data):
        master_id, full_name, phone, experience, login, password = data
        master = Master(
            master_id=master_id,
            full_name=full_name,
            phone=phone,
            experience=experience,
            login=login
        )
        master.set_password(password)
        master.save()
        self.stdout.write(self.style.SUCCESS(f"Создан мастер: {full_name}"))

    def create_service(self, data):
        service_id, info, price = data
        service = Service(service_id=service_id, info=info, price=price)
        service.save()
        self.stdout.write(self.style.SUCCESS(f"Создана услуга: {info}"))

    def create_appointment(self, data):
        appointment_id, client_id, date, time, service_id, master_id, status = data
        client = Client.objects.get(client_id=client_id)
        service = Service.objects.get(service_id=service_id)
        master = Master.objects.get(master_id=master_id)
        appointment = Appointment(
            appointment_id=appointment_id,
            client=client,
            date=date,
            time=time,
            service=service,
            master=master,
            status=status
        )
        appointment.save()
        self.stdout.write(self.style.SUCCESS(f"Создана запись: {appointment_id}"))