from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('usuarios:login'), name='home'),
    path('usuarios/', include('apps.usuarios.urls')),
    path('reservas/', include('apps.reservas.urls')),

    path('informes/', include('apps.informes.urls')),
    path('salas/', include('apps.salas.urls')),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

# Personalizar el admin
admin.site.site_header = 'Sistema de Agendamiento SENA'
admin.site.site_title = 'Sala de Juntas'
admin.site.index_title = 'Administración del Sistema'
