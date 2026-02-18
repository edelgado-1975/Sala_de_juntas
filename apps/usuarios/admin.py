from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Area

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Administrador personalizado para el modelo Usuario
    """
    list_display = ['username', 'email', 'documento', 'tipo_usuario', 'is_active', 'is_staff']
    list_filter = ['tipo_usuario', 'is_active', 'is_staff', 'fecha_creacion']
    search_fields = ['username', 'email', 'documento', 'first_name', 'last_name']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información SENA', {
            'fields': ('documento', 'telefono', 'area_dependencia', 'tipo_usuario', 'foto')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información SENA', {
            'fields': ('documento', 'telefono', 'area_dependencia', 'tipo_usuario')
        }),
    )
