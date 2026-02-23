from .models import Reserva, Sala
from .forms import ReservaForm
from .notifications import notificar_reserva_creada, notificar_reserva_actualizada, notificar_reserva_cancelada
from django.utils.timezone import localtime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from icalendar import Calendar, Event
import uuid

@login_required
def dashboard_view(request):
    """
    Vista principal del dashboard con el calendario de reservas.
    Maneja también la creación rápida de reservas.
    """
    salas = Sala.objects.filter(activa=True).select_related()
    
    if request.method == 'POST':
        if request.user.es_consulta:
            messages.error(request, 'Su perfil es de SOLO CONSULTA. No tiene permisos para crear reservas.')
            return redirect('reservas:dashboard')
            
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user
            reserva.estado = 'CONFIRMADA'
            try:
                reserva.save()
                notificar_reserva_creada(reserva)
                messages.success(request, 'Reserva creada exitosamente.')
                return redirect('reservas:dashboard')
            except Exception as e:
                messages.error(request, f'Error al crear reserva: {str(e)}')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = ReservaForm()

    context = {
        'salas': salas,
        'form': form,
    }
    return render(request, 'reservas/dashboard.html', context)

@login_required
def reservas_api(request):
    """
    API endpoint para obtener las reservas en formato JSON para FullCalendar.
    Permite filtrar por sala si se pasa el parámetro 'sala_id'.
    """
    start = request.GET.get('start')
    end = request.GET.get('end')
    sala_id = request.GET.get('sala_id')
    
    estado_filtro = request.GET.get('estado')
    
    # Si hay un filtro de estado específico, lo usamos.
    # Si no, por defecto mostramos CONFIRMADA y PENDIENTE (para no saturar).
    # Pero si el filtro permite "Todas" o "Cancelada", el API debe responder.
    if estado_filtro:
        reservas = Reserva.objects.filter(estado=estado_filtro)
    else:
        reservas = Reserva.objects.filter(estado__in=['CONFIRMADA', 'PENDIENTE'])

    reservas = reservas.filter(
        fecha_inicio__gte=start,
        fecha_fin__lte=end
    ).select_related('sala', 'usuario')
    
    if sala_id:
        reservas = reservas.filter(sala_id=sala_id)
        
    eventos = []
    for reserva in reservas:
        if reserva.usuario == request.user:
            color = '#007bff'  # Azul para mis reservas
        elif reserva.estado == 'PENDIENTE':
            color = '#ffc107'  # Amarillo para pendientes
        elif reserva.estado == 'CANCELADA':
            color = '#dc3545'  # Rojo para canceladas
        else:
            color = '#28a745'  # Verde para confirmadas
            
        eventos.append({
            'id': reserva.id,
            'title': f"{reserva.sala.nombre} - {reserva.proposito}",
            'start': localtime(reserva.fecha_inicio).isoformat(),
            'end': localtime(reserva.fecha_fin).isoformat(),
            'backgroundColor': color,
            'borderColor': color,
            'extendedProps': {
                'sala': reserva.sala.nombre,
                'usuario': reserva.usuario.get_full_name(),
                'usuario_id': reserva.usuario.id,
                'descripcion': reserva.descripcion,
                'estado': reserva.get_estado_display()
            }
        })
        
    return JsonResponse(eventos, safe=False)
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class ReservaUpdateView(UpdateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'reservas/form_reserva.html'
    success_url = reverse_lazy('reservas:dashboard')

    def get_queryset(self):
        # Solo permitir editar reservas propias o si es superusuario
        qs = super().get_queryset()
        if self.request.user.es_superusuario:
            return qs
        if self.request.user.es_operativo:
            return qs.filter(usuario=self.request.user)
        # Si es CONSULTA o cualquier otro caso no contemplado, no ve nada
        return qs.none()

    def form_valid(self, form):
        messages.success(self.request, 'Reserva actualizada exitosamente.')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class ReservaDeleteView(DeleteView):
    model = Reserva
    template_name = 'reservas/confirmar_eliminar.html'
    success_url = reverse_lazy('reservas:dashboard')

    def get_queryset(self):
        # Solo permitir eliminar reservas propias o si es superusuario
        qs = super().get_queryset()
        if self.request.user.es_superusuario:
            return qs
        if self.request.user.es_operativo:
            return qs.filter(usuario=self.request.user)
        return qs.none()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Reserva eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)

@login_required
def exportar_reserva_ics(request, pk):
    """
    Genera un archivo .ics para una reserva específica.
    """
    reserva = get_object_or_404(Reserva, pk=pk)
    
    # Crear el calendario
    cal = Calendar()
    cal.add('prodid', '-//SENA//Sistema Sala de Juntas//ES')
    cal.add('version', '2.0')
    cal.add('method', 'PUBLISH')
    
    # Crear el evento
    event = Event()
    event.add('summary', f"Reserva: {reserva.proposito}")
    event.add('dtstart', reserva.fecha_inicio)
    event.add('dtend', reserva.fecha_fin)
    event.add('dtstamp', reserva.fecha_creacion)
    
    desc = f"Sala: {reserva.sala.nombre}\n"
    desc += f"Propósito: {reserva.proposito}\n"
    if reserva.descripcion:
        desc += f"Descripción: {reserva.descripcion}\n"
    desc += f"Organizador: {reserva.usuario.get_full_name()}"
    
    event.add('description', desc)
    event.add('location', reserva.sala.ubicacion)
    event.add('uid', f"{reserva.id}-{uuid.uuid4()}@sena.edu.co")
    event.add('status', 'CONFIRMED')
    
    # Añadir evento al calendario
    cal.add_component(event)
    
    # Preparar la respuesta
    response = HttpResponse(cal.to_ical(), content_type="text/calendar")
    response['Content-Disposition'] = f'attachment; filename="reserva_{reserva.id}.ics"'
    
@login_required
def mis_reservas_view(request):
    """
    Vista que muestra las reservas realizadas por el usuario actual.
    Permite filtrar por estado.
    """
    estado = request.GET.get('estado')
    reservas = Reserva.objects.filter(usuario=request.user)
    
    if estado:
        reservas = reservas.filter(estado=estado)
        
    reservas = reservas.select_related('sala').order_by('-fecha_inicio')
    
    context = {
        'reservas': reservas,
        'estado_actual': estado,
    }
    return render(request, 'reservas/mis_reservas.html', context)
