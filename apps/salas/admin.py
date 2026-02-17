from django.contrib import admin
from .models import Sala

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    """
    Administrador para el modelo Sala
    """
    list_display = ['nombre', 'capacidad', 'ubicacion', 'estado', 'activa']
    list_filter = ['estado', 'activa', 'fecha_creacion']
    search_fields = ['nombre', 'ubicacion', 'equipamiento']
    list_editable = ['activa']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'imagen')
        }),
        ('Detalles', {
            'fields': ('capacidad', 'ubicacion', 'equipamiento')
        }),
        ('Horario', {
            'fields': ('hora_apertura', 'hora_cierre')
        }),
        ('Estado', {
            'fields': ('estado', 'activa')
        }),
    )
