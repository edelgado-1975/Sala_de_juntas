
import os
import django
from django.core.mail import send_mail
from django.conf import settings

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salajuntas.settings')
django.setup()

def test_email():
    print(f"Probando envío de email desde: {settings.EMAIL_HOST_USER}")
    try:
        send_mail(
            'Prueba de Conexión - Sistema Sala de Juntas',
            'Este es un mensaje de prueba para verificar la configuración del correo electrónico.',
            settings.DEFAULT_FROM_EMAIL,
            [settings.EMAIL_HOST_USER], # Enviar a sí mismo para probar
            fail_silently=False,
        )
        print("✅ ¡Email enviado exitosamente!")
        print("Revisa tu bandeja de entrada (y la carpeta de Spam).")
    except Exception as e:
        print("❌ Error al enviar el email:")
        print(str(e))

if __name__ == "__main__":
    test_email()
