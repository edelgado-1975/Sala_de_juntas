from django import forms
from .models import Reserva, Sala
from django.utils import timezone

class ReservaForm(forms.ModelForm):
    """
    Formulario para crear y editar reservas.
    """
    class Meta:
        model = Reserva
        fields = ['sala', 'fecha_inicio', 'fecha_fin', 'proposito', 'descripcion', 'num_asistentes', 'estado']
        widgets = {
            'sala': forms.Select(attrs={'class': 'form-select'}),
            'fecha_inicio': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'fecha_fin': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'proposito': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Reunión de equipo'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'num_asistentes': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo salas activas
        self.fields['sala'].queryset = Sala.objects.filter(activa=True)
        # Asegurar que el formato sea reconocido por el widget datetime-local
        self.fields['fecha_inicio'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['fecha_fin'].input_formats = ['%Y-%m-%dT%H:%M']

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        sala = cleaned_data.get('sala')
        num_asistentes = cleaned_data.get('num_asistentes')

        if fecha_inicio and fecha_fin:
            # Solo validar "en el pasado" si es una nueva reserva (margen 5 min)
            now_minus_5 = timezone.now() - timezone.timedelta(minutes=5)
            if not self.instance.pk and fecha_inicio < now_minus_5:
                self.add_error('fecha_inicio', 'La fecha de inicio no puede ser en el pasado.')
            
            if fecha_fin <= fecha_inicio:
                self.add_error('fecha_fin', 'La fecha de fin debe ser posterior a la de inicio.')

        # 1. Validación de Horarios de Operación (7:00 AM - 9:30 PM)
        if fecha_inicio and fecha_fin:
            if fecha_inicio.hour < 7 or (fecha_inicio.hour >= 21 and fecha_inicio.minute > 30) or fecha_inicio.hour > 21:
                self.add_error('fecha_inicio', '🕒 El sistema solo permite agendamientos entre las 07:00 AM y las 09:30 PM.')
            if fecha_fin.hour > 21 or (fecha_fin.hour == 21 and fecha_fin.minute > 30):
                self.add_error('fecha_fin', '🕒 La hora de finalización no puede exceder las 09:30 PM.')

        # 2. Límites de Anticipación (Min 1h, Max 90 días)
        if fecha_inicio and not self.instance.pk:
            ahora = timezone.now()
            if fecha_inicio < ahora + timezone.timedelta(hours=1):
                self.add_error('fecha_inicio', '⏳ Las reservas deben realizarse con al menos 1 hora de anticipación.')
            if fecha_inicio > ahora + timezone.timedelta(days=90):
                self.add_error('fecha_inicio', '📅 No se permiten reservas con más de 90 días de anticipación.')

        # 3. Optimización de Capacidad (Sub-utilización)
        if sala and num_asistentes:
            if num_asistentes > sala.capacidad:
                self.add_error('num_asistentes', f'La capacidad máxima de la sala {sala.nombre} es de {sala.capacidad} personas.')
            
            # Bloquear sub-utilización extrema (menos del 10% de la capacidad)
            minimo_requerido = max(1, round(sala.capacidad * 0.1))
            if num_asistentes < minimo_requerido:
                self.add_error('num_asistentes', f'⚠️ Eficiencia de espacio: Para {num_asistentes} personas, por favor use un espacio más pequeño o un cubículo. El mínimo para esta sala es de {minimo_requerido} personas.')

        # 4. Validación de Solapamiento y Tiempo de Gracia (15 min)
        if sala and fecha_inicio and fecha_fin:
            # Buffer de 15 minutos (Directiva de Calidad)
            buffer = timezone.timedelta(minutes=15)
            check_inicio = fecha_inicio - buffer
            check_fin = fecha_fin + buffer

            solapamientos = Reserva.objects.filter(
                sala=sala,
                fecha_inicio__lt=check_fin,
                fecha_fin__gt=check_inicio
            ).exclude(estado='CANCELADA')

            if self.instance.pk:
                solapamientos = solapamientos.exclude(pk=self.instance.pk)

            if solapamientos.exists():
                error_msg = f'⚠️ Conflicto de horario: Existe otra reserva muy cercana o solapada. Recuerde que debe existir un margen de 15 minutos entre reuniones para limpieza y entrega de la sala.'
                self.add_error('fecha_inicio', error_msg)
                self.add_error('fecha_fin', error_msg)

        return cleaned_data
