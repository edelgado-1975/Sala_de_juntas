from django.urls import path
from . import views

app_name = 'salas'

urlpatterns = [
    path('', views.SalaListView.as_view(), name='lista'),
    path('nueva/', views.SalaCreateView.as_view(), name='crear'),
    path('editar/<int:pk>/', views.SalaUpdateView.as_view(), name='editar'),
    path('eliminar/<int:pk>/', views.SalaDeleteView.as_view(), name='eliminar'),
]
