from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Sala, Reserva
from .forms import ReservaForm
import datetime

User = get_user_model()

class ReservaQATestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpassword',
            email='test@example.com',
            documento='12345'
        )
        self.sala = Sala.objects.create(
            nombre='Sala de Prueba',
            capacidad=20,
            ubicacion='Piso 1',
            activa=True
        )

    def get_future_datetime(self, days=1, hour=10, minutes=0):
        dt = timezone.now() + timezone.timedelta(days=days)
        return dt.replace(hour=hour, minute=minutes, second=0, microsecond=0)

    def test_operacion_horario_valido(self):
        """Verificar que se permite reservar dentro del horario (7 AM - 9:30 PM)"""
        inicio = self.get_future_datetime(hour=8, minutes=0)
        fin = self.get_future_datetime(hour=9, minutes=0)
        
        form_data = {
            'sala': self.sala.id,
            'fecha_inicio': inicio.strftime('%Y-%m-%dT%H:%M'),
            'fecha_fin': fin.strftime('%Y-%m-%dT%H:%M'),
            'proposito': 'Reunión válida',
            'num_asistentes': 5,
            'estado': 'CONFIRMADA'
        }
        form = ReservaForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_operacion_horario_invalido_temprano(self):
        """Verificar bloqueo antes de las 7:00 AM"""
        inicio = self.get_future_datetime(hour=6, minutes=30)
        fin = self.get_future_datetime(hour=7, minutes=30)
        
        form_data = {
            'sala': self.sala.id,
            'fecha_inicio': inicio.strftime('%Y-%m-%dT%H:%M'),
            'fecha_fin': fin.strftime('%Y-%m-%dT%H:%M'),
            'proposito': 'Reunión muy temprano',
            'num_asistentes': 5,
            'estado': 'CONFIRMADA'
        }
        form = ReservaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('fecha_inicio', form.errors)

    def test_operacion_horario_invalido_tarde(self):
        """Verificar bloqueo después de las 9:30 PM"""
        inicio = self.get_future_datetime(hour=21, minutes=40)
        fin = self.get_future_datetime(hour=22, minutes=40)
        
        form_data = {
            'sala': self.sala.id,
            'fecha_inicio': inicio.strftime('%Y-%m-%dT%H:%M'),
            'fecha_fin': fin.strftime('%Y-%m-%dT%H:%M'),
            'proposito': 'Reunión muy tarde',
            'num_asistentes': 5,
            'estado': 'CONFIRMADA'
        }
        form = ReservaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('fecha_inicio', form.errors)

    def test_anticipacion_minima(self):
        """Verificar que se requiere al menos 1 hora de anticipación"""
        ahora = timezone.now()
        inicio = ahora + timezone.timedelta(minutes=30)
        fin = inicio + timezone.timedelta(hours=1)
        
        form_data = {
            'sala': self.sala.id,
            'fecha_inicio': inicio.strftime('%Y-%m-%dT%H:%M'),
            'fecha_fin': fin.strftime('%Y-%m-%dT%H:%M'),
            'proposito': 'Reunión sin anticipación',
            'num_asistentes': 5,
            'estado': 'CONFIRMADA'
        }
        form = ReservaForm(data=form_data)
        # Nota: La validación usa timezone.now(), por lo que en el test 
        # debemos ser cuidadosos con el tiempo exacto.
        self.assertFalse(form.is_valid())
        self.assertIn('fecha_inicio', form.errors)

    def test_buffer_entre_reservas(self):
        """Verificar que se respeta el buffer de 15 minutos"""
        # Primera reserva: 10:00 AM - 11:00 AM
        inicio1 = self.get_future_datetime(hour=10, minutes=0)
        fin1 = self.get_future_datetime(hour=11, minutes=0)
        Reserva.objects.create(
            usuario=self.user,
            sala=self.sala,
            fecha_inicio=inicio1,
            fecha_fin=fin1,
            proposito='Reserva 1',
            num_asistentes=5
        )
        
        # Intento de reserva 2: 11:10 AM - 12:00 PM (Solo 10 min de buffer, debe fallar)
        inicio2 = self.get_future_datetime(hour=11, minutes=10)
        fin2 = self.get_future_datetime(hour=12, minutes=0)
        
        form_data = {
            'sala': self.sala.id,
            'fecha_inicio': inicio2.strftime('%Y-%m-%dT%H:%M'),
            'fecha_fin': fin2.strftime('%Y-%m-%dT%H:%M'),
            'proposito': 'Reserva con poco buffer',
            'num_asistentes': 5,
            'estado': 'CONFIRMADA'
        }
        form = ReservaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('fecha_inicio', form.errors)
        self.assertIn('Conflicto de horario', form.errors['fecha_inicio'][0])

    def test_subutilizacion_extrema(self):
        """Verificar bloqueo si el aforo es menor al 10% (Capacidad 20, 1 persona = 5%)"""
        inicio = self.get_future_datetime(hour=14, minutes=0)
        fin = self.get_future_datetime(hour=15, minutes=0)
        
        form_data = {
            'sala': self.sala.id,
            'fecha_inicio': inicio.strftime('%Y-%m-%dT%H:%M'),
            'fecha_fin': fin.strftime('%Y-%m-%dT%H:%M'),
            'proposito': 'Reunión subutilizada',
            'num_asistentes': 1, # 1/20 = 5% < 10%
            'estado': 'CONFIRMADA'
        }
        form = ReservaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('num_asistentes', form.errors)
        self.assertIn('Eficiencia de espacio', form.errors['num_asistentes'][0])

    def test_capacidad_maxima(self):
        """Verificar que no se exceda la capacidad de la sala"""
        inicio = self.get_future_datetime(hour=16, minutes=0)
        fin = self.get_future_datetime(hour=17, minutes=0)
        
        form_data = {
            'sala': self.sala.id,
            'fecha_inicio': inicio.strftime('%Y-%m-%dT%H:%M'),
            'fecha_fin': fin.strftime('%Y-%m-%dT%H:%M'),
            'proposito': 'Reunión multitudinaria',
            'num_asistentes': 25, # Capacidad es 20
            'estado': 'CONFIRMADA'
        }
        form = ReservaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('num_asistentes', form.errors)
