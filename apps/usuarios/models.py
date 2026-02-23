from django.db import models
from django.contrib.auth.models import AbstractUser

class Area(models.Model):
    """
    Modelo para las Áreas o Dependencias del SENA.
    Permite que el administrador configure las opciones disponibles.
    """
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre del Área'
    )
    
    class Meta:
        verbose_name = 'Área/Dependencia'
        verbose_name_plural = 'Áreas/Dependencias'
        ordering = ['nombre']
        
    def __str__(self):
        return self.nombre

class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado para el sistema de agendamiento.
    Extiende AbstractUser para agregar campos específicos del SENA.
    """
    
    TIPO_USUARIO_CHOICES = [
        ('SUPERUSUARIO', 'Super Usuario'),
        ('OPERATIVO', 'Operativo'),
        ('CONSULTA', 'Consulta'),
    ]
    
    documento = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Documento de Identidad',
        help_text='Número de documento sin puntos ni comas'
    )
    
    telefono = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Teléfono'
    )
    
    area_dependencia = models.ForeignKey(
        Area,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Área/Dependencia SENA',
        help_text='Seleccione el área o dependencia a la que pertenece'
    )
    
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPO_USUARIO_CHOICES,
        default='CONSULTA',
        verbose_name='Tipo de Usuario'
    )
    
    foto = models.ImageField(
        upload_to='usuarios/fotos/',
        blank=True,
        null=True,
        verbose_name='Foto de Perfil'
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
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.documento})"
    
    def get_full_name(self):
        """Retorna el nombre completo del usuario"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    @property
    def es_superusuario(self):
        """Verifica si el usuario es superusuario"""
        return self.is_superuser or self.tipo_usuario == 'SUPERUSUARIO'

    @property
    def es_operativo(self):
        """Verifica si el usuario tiene rol operativo"""
        return self.tipo_usuario == 'OPERATIVO'

    @property
    def es_consulta(self):
        """Verifica si el usuario tiene rol de consulta"""
        return self.tipo_usuario == 'CONSULTA'

    @property
    def es_administrador(self):
        """Verifica si el usuario tiene permisos administrativos"""
        return self.es_superusuario

class LogSeguridad(models.Model):
    """
    Modelo para registrar eventos de seguridad (ej. fallos de login)
    """
    TIPO_EVENTO_CHOICES = [
        ('LOGIN_FALLIDO', 'Inicio de Sesión Fallido'),
        ('ACCESO_DENEGADO', 'Acceso Denegado'),
    ]
    
    fecha = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y Hora')
    usuario_intentado = models.CharField(max_length=150, blank=True, null=True, verbose_name='Usuario Intentado')
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name='Dirección IP')
    tipo_evento = models.CharField(max_length=20, choices=TIPO_EVENTO_CHOICES, verbose_name='Tipo de Evento')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    
    class Meta:
        verbose_name = 'Log de Seguridad'
        verbose_name_plural = 'Logs de Seguridad'
        ordering = ['-fecha']
        
    def __str__(self):
        return f"{self.tipo_evento} - {self.usuario_intentado} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"
