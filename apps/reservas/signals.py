from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Reserva, HistorialReserva

@receiver(post_save, sender=Reserva)
def registrar_historial_y_notificar_guardado(sender, instance, created, **kwargs):
    from .notifications import notificar_reserva_creada, notificar_reserva_actualizada, notificar_reserva_cancelada
    
    accion = 'CREADA' if created else 'MODIFICADA'
    descripcion = f"La reserva fue {accion.lower()}."
    
    if instance.estado == 'CANCELADA':
        accion = 'CANCELADA'
        descripcion = "La reserva fue marcada como cancelada."
        notificar_reserva_cancelada(instance)
    elif instance.estado == 'COMPLETADA':
        accion = 'COMPLETADA'
        descripcion = "La reserva fue marcada como completada."
    elif created:
        notificar_reserva_creada(instance)
    else:
        # Notificar actualización genérica (solo si no es cancelación/completado)
        notificar_reserva_actualizada(instance)

    HistorialReserva.objects.create(
        reserva=instance,
        usuario=instance.usuario,  # Nota: Esto asocia la acción al dueño de la reserva
        accion=accion,
        descripcion=descripcion
    )

@receiver(post_delete, sender=Reserva)
def registrar_historial_y_notificar_eliminado(sender, instance, **kwargs):
    """
    Notifica la cancelación por email cuando se elimina físicamente el registro,
    ya sea desde la vista o desde el administrador de Django.
    """
    from .notifications import notificar_reserva_cancelada
    
    # Notificar por email
    try:
        notificar_reserva_cancelada(instance)
    except Exception:
        pass # Evitar que un fallo en email bloquee la eliminación
