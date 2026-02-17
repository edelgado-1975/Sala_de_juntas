from django.db import models

class Sala(models.Model):
    """
    Modelo para las salas de juntas disponibles en el SENA
    """
    
    ESTADO_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
        ('MANTENIMIENTO', 'En Mantenimiento'),
        ('FUERA_SERVICIO', 'Fuera de Servicio'),
    ]
    
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre de la Sala'
    )
    
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción'
    )
    
    capacidad = models.PositiveIntegerField(
        verbose_name='Capacidad (personas)',
        help_text='Número máximo de personas que puede albergar la sala'
    )
    
    ubicacion = models.CharField(
        max_length=150,
        verbose_name='Ubicación',
        help_text='Ejemplo: Edificio A, Piso 2'
    )
    
    equipamiento = models.TextField(
        blank=True,
        null=True,
        verbose_name='Equipamiento Disponible',
        help_text='Proyector, videoconferencia, pizarra, etc.'
    )
    
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='DISPONIBLE',
        verbose_name='Estado'
    )
    
    imagen = models.ImageField(
        upload_to='salas/',
        blank=True,
        null=True,
        verbose_name='Imagen de la Sala'
    )
    
    hora_apertura = models.TimeField(
        default='07:00',
        verbose_name='Hora de Apertura',
        help_text='Hora en que la sala está disponible desde'
    )
    
    hora_cierre = models.TimeField(
        default='18:00',
        verbose_name='Hora de Cierre',
        help_text='Hora en que la sala cierra'
    )
    
    activa = models.BooleanField(
        default=True,
        verbose_name='Activa',
        help_text='Indica si la sala está activa para reservas'
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
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} (Cap: {self.capacidad})"
    
    @property
    def esta_disponible(self):
        """Verifica si la sala está disponible para reservas"""
        return self.activa and self.estado == 'DISPONIBLE'
