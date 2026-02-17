from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Reserva, Sala
from .forms import ReservaForm
from django.utils.timezone import localtime

@login_required
def dashboard_view(request):
    """
    Vista principal del dashboard con el calendario de reservas.
    Maneja también la creación rápida de reservas.
    """
    salas = Sala.objects.filter(activa=True)
    
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user
            reserva.estado = 'CONFIRMADA'
            try:
                reserva.save()
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
    
    reservas = Reserva.objects.filter(
        estado__in=['CONFIRMADA', 'PENDIENTE'],
        fecha_inicio__gte=start,
        fecha_fin__lte=end
    ).select_related('sala', 'usuario')
    
    if sala_id:
        reservas = reservas.filter(sala_id=sala_id)
        
    eventos = []
    for reserva in reservas:
        color = '#28a745'  # Verde por defecto (Confirmada)
        if reserva.estado == 'PENDIENTE':
            color = '#ffc107'  # Amarillo
        elif reserva.usuario == request.user:
            color = '#007bff'  # Azul para mis reservas
            
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
        # Solo permitir editar reservas propias o si es admin
        qs = super().get_queryset()
        if self.request.user.is_staff or self.request.user.tipo_usuario == 'COORDINADOR':
            return qs
        return qs.filter(usuario=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Reserva actualizada exitosamente.')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class ReservaDeleteView(DeleteView):
    model = Reserva
    template_name = 'reservas/confirmar_eliminar.html'
    success_url = reverse_lazy('reservas:dashboard')

    def get_queryset(self):
        # Solo permitir eliminar reservas propias o si es admin
        qs = super().get_queryset()
        if self.request.user.is_staff or self.request.user.tipo_usuario == 'COORDINADOR':
            return qs
        return qs.filter(usuario=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Reserva eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)
