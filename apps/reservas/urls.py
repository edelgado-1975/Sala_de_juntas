from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('mis-reservas/', views.mis_reservas_view, name='mis_reservas'),
    path('api/eventos/', views.reservas_api, name='api_eventos'),
    path('editar/<int:pk>/', views.ReservaUpdateView.as_view(), name='editar'),
    path('eliminar/<int:pk>/', views.ReservaDeleteView.as_view(), name='eliminar'),
    path('exportar/<int:pk>/', views.exportar_reserva_ics, name='exportar_ics'),
]
