from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import LoginForm, PerfilForm, RegistroUserForm


from .models import LogSeguridad

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def login_view(request):
    """Vista de inicio de sesión"""
    if request.user.is_authenticated:
        return redirect('reservas:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        username = request.POST.get('username')
        if form.is_valid():
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {user.get_full_name()}!')
                
                # Redirigir a la página solicitada o al dashboard
                next_url = request.GET.get('next', 'reservas:dashboard')
                return redirect(next_url)
        else:
            # Registrar fallo de seguridad
            LogSeguridad.objects.create(
                usuario_intentado=username,
                ip_address=get_client_ip(request),
                tipo_evento='LOGIN_FALLIDO',
                descripcion='Intento de inicio de sesión con credenciales incorrectas.'
            )
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    
    return render(request, 'usuarios/login.html', {'form': form})


def logout_view(request):
    """Vista de cierre de sesión"""
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('usuarios:login')


@login_required
def perfil_view(request):
    """Vista de perfil de usuario"""
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('usuarios:perfil')
    else:
        form = PerfilForm(instance=request.user)
    
    return render(request, 'usuarios/perfil.html', {'form': form})


def registro_view(request):
    """Vista de registro de nuevos usuarios"""
    if request.user.is_authenticated:
        return redirect('reservas:dashboard')
        
    if request.method == 'POST':
        form = RegistroUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Login automatico tras registro
            messages.success(request, f'¡Registro exitoso! Bienvenido {user.get_full_name()}.')
            return redirect('reservas:dashboard')
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        form = RegistroUserForm()
        
    return render(request, 'usuarios/registro.html', {'form': form})
