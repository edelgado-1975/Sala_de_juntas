from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum
from django.utils import timezone
from apps.reservas.models import Reserva
from apps.salas.models import Sala
from apps.usuarios.models import Usuario
import calendar
from datetime import datetime, timedelta

def es_admin(user):
    return user.is_staff or user.tipo_usuario == 'COORDINADOR'

@login_required
@user_passes_test(es_admin)
def dashboard_informes(request):
    """
    Vista principal del dashboard de informes y estadísticas.
    """
    total_salas = Sala.objects.count()
    total_usuarios = Usuario.objects.count()
    total_reservas = Reserva.objects.count()
    reservas_hoy = Reserva.objects.filter(
        fecha_inicio__date=timezone.now().date()
    ).count()

    # Estadísticas por sala
    reservas_por_sala = Reserva.objects.values('sala__nombre').annotate(
        total=Count('id')
    ).order_by('-total')

    # Estadísticas por estado
    reservas_por_estado = Reserva.objects.values('estado').annotate(
        total=Count('id')
    )

    context = {
        'total_salas': total_salas,
        'total_usuarios': total_usuarios,
        'total_reservas': total_reservas,
        'reservas_hoy': reservas_hoy,
        'reservas_por_sala': reservas_por_sala,
        'reservas_por_estado': reservas_por_estado,
    }
    return render(request, 'informes/dashboard.html', context)
