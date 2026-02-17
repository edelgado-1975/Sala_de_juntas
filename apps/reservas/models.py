from django.db import models
from django.conf import settings
from apps.salas.models import Sala
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.timezone import localtime

class Reserva(models.Model):
    """
    Modelo para las reservas de salas de juntas
    """
    
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
        ('COMPLETADA', 'Completada'),
    ]
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservas',
        verbose_name='Usuario'
    )
    
    sala = models.ForeignKey(
        Sala,
        on_delete=models.CASCADE,
        related_name='reservas',
        verbose_name='Sala'
    )
    
    fecha_inicio = models.DateTimeField(
        verbose_name='Fecha y Hora de Inicio'
    )
    
    fecha_fin = models.DateTimeField(
        verbose_name='Fecha y Hora de Fin'
    )
    
    proposito = models.CharField(
        max_length=200,
        verbose_name='Propósito de la Reunión',
        help_text='Breve descripción del propósito'
    )
    
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción Detallada'
    )
    
    num_asistentes = models.PositiveIntegerField(
        verbose_name='Número de Asistentes',
        help_text='Cantidad de personas que asistirán'
    )
    
    estado = models.CharField(
        max_length=15,
        choices=ESTADO_CHOICES,
        default='CONFIRMADA',
        verbose_name='Estado'
    )
    
    notas = models.TextField(
        blank=True,
        null=True,
        verbose_name='Notas Adicionales'
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Actualización'
    )
    
    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-fecha_inicio']
        indexes = [
            models.Index(fields=['fecha_inicio', 'fecha_fin']),
            models.Index(fields=['sala', 'estado']),
        ]
    
    def __str__(self):
        return f"{self.sala.nombre} - {self.fecha_inicio.strftime('%d/%m/%Y %H:%M')} - {self.usuario.get_full_name()}"
    
    def clean(self):
        """Validaciones personalizadas"""
        # Validar que fecha_fin sea posterior a fecha_inicio
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_fin <= self.fecha_inicio:
                raise ValidationError('La fecha de fin debe ser posterior a la fecha de inicio.')
            
            # Validar que la reserva no sea en el pasado (con margen de 5 min para procesamiento)
            if not self.pk and self.fecha_inicio < (timezone.now() - timezone.timedelta(minutes=5)):
                raise ValidationError('No se pueden crear reservas en el pasado.')
            
            # Validar que la reserva esté dentro del horario de la sala
            if self.sala:
                # Importante: convertir a hora local antes de comparar con TimeField
                hora_inicio = localtime(self.fecha_inicio).time()
                hora_fin = localtime(self.fecha_fin).time()
                
                if hora_inicio < self.sala.hora_apertura:
                    raise ValidationError(f'La sala abre a las {self.sala.hora_apertura}.')
                if hora_fin > self.sala.hora_cierre:
                    raise ValidationError(f'La sala cierra a las {self.sala.hora_cierre}.')
        
        # Validar capacidad
        if self.sala and self.num_asistentes:
            if self.num_asistentes > self.sala.capacidad:
                raise ValidationError(
                    f'El número de asistentes ({self.num_asistentes}) excede la capacidad de la sala ({self.sala.capacidad}).'
                )
        
        # Validar que no haya conflictos con otras reservas
        if self.sala and self.fecha_inicio and self.fecha_fin:
            conflictos = Reserva.objects.filter(
                sala=self.sala,
                estado__in=['CONFIRMADA', 'PENDIENTE'],
                fecha_inicio__lt=self.fecha_fin,
                fecha_fin__gt=self.fecha_inicio
            ).exclude(pk=self.pk)
            
            if conflictos.exists():
                raise ValidationError('Ya existe una reserva para esta sala en el horario seleccionado.')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def duracion_horas(self):
        """Calcula la duración de la reserva en horas"""
        if self.fecha_inicio and self.fecha_fin:
            duracion = self.fecha_fin - self.fecha_inicio
            return duracion.total_seconds() / 3600
        return 0
    
    @property
    def esta_activa(self):
        """Verifica si la reserva está activa"""
        return self.fecha_inicio <= timezone.now() <= self.fecha_fin and self.estado == 'CONFIRMADA'


class HistorialReserva(models.Model):
    """
    Modelo para auditoría de cambios en reservas
    """
    
    ACCION_CHOICES = [
        ('CREADA', 'Creada'),
        ('MODIFICADA', 'Modificada'),
        ('CANCELADA', 'Cancelada'),
        ('COMPLETADA', 'Completada'),
    ]
    
    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.CASCADE,
        related_name='historial',
        verbose_name='Reserva'
    )
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Usuario que Realizó la Acción'
    )
    
    accion = models.CharField(
        max_length=15,
        choices=ACCION_CHOICES,
        verbose_name='Acción'
    )
    
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción del Cambio'
    )
    
    fecha = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de la Acción'
    )
    
    class Meta:
        verbose_name = 'Historial de Reserva'
        verbose_name_plural = 'Historial de Reservas'
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.reserva} - {self.accion} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"
