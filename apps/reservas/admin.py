from django.contrib import admin
from .models import Reserva, HistorialReserva

class HistorialReservaInline(admin.TabularInline):
    """Inline para mostrar historial de reserva"""
    model = HistorialReserva
    extra = 0
    readonly_fields = ['usuario', 'accion', 'descripcion', 'fecha']
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    """
    Administrador para el modelo Reserva
    """
    list_display = ['sala', 'usuario', 'fecha_inicio', 'fecha_fin', 'num_asistentes', 'estado', 'duracion_display']
    list_filter = ['estado', 'fecha_inicio', 'sala']
    search_fields = ['usuario__username', 'usuario__first_name', 'usuario__last_name', 'proposito', 'sala__nombre']
    date_hierarchy = 'fecha_inicio'
    list_editable = ['estado']
    inlines = [HistorialReservaInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('usuario', 'sala', 'estado')
        }),
        ('Fechas y Horarios', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
        ('Detalles de la Reunión', {
            'fields': ('proposito', 'descripcion', 'num_asistentes')
        }),
        ('Notas', {
            'fields': ('notas',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    def duracion_display(self, obj):
        """Muestra la duración de la reserva"""
        return f"{obj.duracion_horas:.1f}h"
    duracion_display.short_description = 'Duración'
    
    def save_model(self, request, obj, form, change):
        """Guarda el modelo y crea historial"""
        super().save_model(request, obj, form, change)
        
        # Crear entrada en historial
        accion = 'MODIFICADA' if change else 'CREADA'
        HistorialReserva.objects.create(
            reserva=obj,
            usuario=request.user,
            accion=accion,
            descripcion=f"Reserva {accion.lower()} por {request.user.get_full_name()}"
        )


@admin.register(HistorialReserva)
class HistorialReservaAdmin(admin.ModelAdmin):
    """
    Administrador para el modelo HistorialReserva
    """
    list_display = ['reserva', 'usuario', 'accion', 'fecha']
    list_filter = ['accion', 'fecha']
    search_fields = ['reserva__proposito', 'usuario__username', 'descripcion']
    readonly_fields = ['reserva', 'usuario', 'accion', 'descripcion', 'fecha']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
