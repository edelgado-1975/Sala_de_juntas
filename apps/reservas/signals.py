from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Reserva, HistorialReserva

@receiver(post_save, sender=Reserva)
def registrar_historial_guardado(sender, instance, created, **kwargs):
    accion = 'CREADA' if created else 'MODIFICADA'
    descripcion = f"La reserva fue {accion.lower()}."
    if instance.estado == 'CANCELADA':
        accion = 'CANCELADA'
        descripcion = "La reserva fue marcada como cancelada."
    elif instance.estado == 'COMPLETADA':
        accion = 'COMPLETADA'
        descripcion = "La reserva fue marcada como completada."

    HistorialReserva.objects.create(
        reserva=instance,
        usuario=instance.usuario,  # Nota: Esto asocia la acción al dueño de la reserva
        accion=accion,
        descripcion=descripcion
    )

@receiver(post_delete, sender=Reserva)
def registrar_historial_eliminado(sender, instance, **kwargs):
    # Nota: El historial se borrará en cascada si se borra la reserva, 
    # a menos que se cambie el on_delete en el modelo.
    # Por ahora, registramos en el log de consola o un archivo externo si fuera necesario.
    pass
