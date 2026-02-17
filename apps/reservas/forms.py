from django import forms
from .models import Reserva, Sala
from django.utils import timezone

class ReservaForm(forms.ModelForm):
    """
    Formulario para crear y editar reservas.
    """
    class Meta:
        model = Reserva
        fields = ['sala', 'fecha_inicio', 'fecha_fin', 'proposito', 'descripcion', 'num_asistentes']
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

        if sala and num_asistentes:
            if num_asistentes > sala.capacidad:
                self.add_error('num_asistentes', f'La capacidad máxima de la sala {sala.nombre} es de {sala.capacidad} personas.')

        return cleaned_data
