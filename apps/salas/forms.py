from django import forms
from .models import Sala

class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['nombre', 'descripcion', 'capacidad', 'ubicacion', 'equipamiento', 'estado', 'imagen', 'hora_apertura', 'hora_cierre', 'activa']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'equipamiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'hora_apertura': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_cierre': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
