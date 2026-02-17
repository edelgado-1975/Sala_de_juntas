from django.urls import path
from . import views

app_name = 'informes'

urlpatterns = [
    path('', views.dashboard_informes, name='dashboard'),
    path('exportar/pdf/', views.exportar_reservas_pdf, name='exportar_pdf'),
    path('exportar/excel/', views.exportar_reservas_excel, name='exportar_excel'),
    path('usuario/', views.informe_usuario_view, name='informe_usuario'),
]
