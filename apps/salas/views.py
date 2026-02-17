from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Sala
from .forms import SalaForm

def es_admin(user):
    return user.is_staff or user.tipo_usuario == 'COORDINADOR'

@method_decorator([login_required, user_passes_test(es_admin)], name='dispatch')
class SalaListView(ListView):
    model = Sala
    template_name = 'salas/lista_salas.html'
    context_object_name = 'salas'

@method_decorator([login_required, user_passes_test(es_admin)], name='dispatch')
class SalaCreateView(CreateView):
    model = Sala
    form_class = SalaForm
    template_name = 'salas/form_sala.html'
    success_url = reverse_lazy('salas:lista')

    def form_valid(self, form):
        messages.success(self.request, 'Sala creada exitosamente.')
        return super().form_valid(form)

@method_decorator([login_required, user_passes_test(es_admin)], name='dispatch')
class SalaUpdateView(UpdateView):
    model = Sala
    form_class = SalaForm
    template_name = 'salas/form_sala.html'
    success_url = reverse_lazy('salas:lista')

    def form_valid(self, form):
        messages.success(self.request, 'Sala actualizada exitosamente.')
        return super().form_valid(form)

@method_decorator([login_required, user_passes_test(es_admin)], name='dispatch')
class SalaDeleteView(DeleteView):
    model = Sala
    template_name = 'salas/confirmar_eliminar.html'
    success_url = reverse_lazy('salas:lista')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Sala eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)
