from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado para el sistema de agendamiento.
    Extiende AbstractUser para agregar campos específicos del SENA.
    """
    
    TIPO_USUARIO_CHOICES = [
        ('INSTRUCTOR', 'Instructor'),
        ('ADMINISTRATIVO', 'Administrativo'),
        ('COORDINADOR', 'Coordinador'),
        ('VISITANTE', 'Visitante'),
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
    
    area_dependencia = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Área/Dependencia SENA',
        help_text='Área o dependencia a la que pertenece en el SENA'
    )
    
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPO_USUARIO_CHOICES,
        default='INSTRUCTOR',
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
    def es_administrador(self):
        """Verifica si el usuario es administrador o coordinador"""
        return self.is_superuser or self.tipo_usuario == 'COORDINADOR'
