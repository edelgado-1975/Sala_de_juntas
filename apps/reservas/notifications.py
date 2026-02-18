"""
notifications.py - Módulo de Notificaciones por Email
Sistema de Agendamiento de Sala de Juntas - SENA
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def _enviar_email(asunto, template_html, contexto, destinatarios):
    """
    Función interna para enviar emails HTML con fallback a texto plano.
    """
    try:
        html_message = render_to_string(template_html, contexto)
        plain_message = strip_tags(html_message)
        send_mail(
            subject=asunto,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=destinatarios,
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Email '{asunto}' enviado a {destinatarios}")
        return True
    except Exception as e:
        logger.error(f"Error al enviar email '{asunto}': {str(e)}")
        return False


def notificar_reserva_creada(reserva):
    """
    Envía notificación al usuario cuando crea una reserva.
    """
    if not reserva.usuario.email:
        return

    contexto = {'reserva': reserva, 'accion': 'creada'}
    _enviar_email(
        asunto=f'✅ Reserva Confirmada - {reserva.sala.nombre} | SENA',
        template_html='emails/reserva_confirmada.html',
        contexto=contexto,
        destinatarios=[reserva.usuario.email],
    )


def notificar_reserva_actualizada(reserva):
    """
    Envía notificación al usuario cuando actualiza una reserva.
    """
    if not reserva.usuario.email:
        return

    contexto = {'reserva': reserva, 'accion': 'actualizada'}
    _enviar_email(
        asunto=f'📝 Reserva Actualizada - {reserva.sala.nombre} | SENA',
        template_html='emails/reserva_actualizada.html',
        contexto=contexto,
        destinatarios=[reserva.usuario.email],
    )


def notificar_reserva_cancelada(reserva):
    """
    Envía notificación al usuario cuando cancela/elimina una reserva.
    """
    if not reserva.usuario.email:
        return

    contexto = {'reserva': reserva, 'accion': 'cancelada'}
    _enviar_email(
        asunto=f'❌ Reserva Cancelada - {reserva.sala.nombre} | SENA',
        template_html='emails/reserva_cancelada.html',
        contexto=contexto,
        destinatarios=[reserva.usuario.email],
    )
