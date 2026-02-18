from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import get_user_model

Usuario = get_user_model()


class LoginForm(AuthenticationForm):
    """Formulario de inicio de sesión personalizado"""
    username = forms.CharField(
        label='Usuario o Documento',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Usuario o Documento',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
    )


class UsuarioCreationForm(UserCreationForm):
    """Formulario para crear usuarios desde el admin"""
    
    class Meta:
        model = Usuario
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'documento', 'telefono', 'area_dependencia', 'tipo_usuario'
        )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'documento': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'area_dependencia': forms.Select(attrs={'class': 'form-control'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-control'}),
        }


class PerfilForm(UserChangeForm):
    """Formulario para editar perfil de usuario"""
    password = None  # No mostrar campo de contraseña
    
    class Meta:
        model = Usuario
        fields = (
            'first_name', 'last_name', 'email',
            'telefono', 'area_dependencia', 'foto'
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'area_dependencia': forms.Select(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }
class RegistroUserForm(UserCreationForm):
    """Formulario para auto-registro de usuarios"""
    
    class Meta:
        model = Usuario
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'documento', 'telefono', 'area_dependencia'
        )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de Usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Documento de Identidad'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'area_dependencia': forms.Select(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Mínimo 4 caracteres (letras, números y @/./+/-/_).'
        self.fields['password1'].help_text = 'Mínimo 8 caracteres. Evite datos personales o secuencias comunes.'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo_usuario = 'CONSULTA'  # Rol por defecto para auto-registro
        if commit:
            user.save()
        return user
