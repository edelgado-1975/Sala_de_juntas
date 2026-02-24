# 🌐 Manual de Despliegue en Hosting Web con Subdominio
## Sistema de Agendamiento de Salas de Juntas - SENA
**Dominio: educaciondigitalsena.com.co | Versión 1.0.0 | Febrero 2026**

---

## 1. Resumen del Plan

Vamos a desplegar la aplicación en un **subdominio** de tu hosting, por ejemplo:
`https://salas.educaciondigitalsena.com.co`

Para esto usaremos **cPanel** (el panel de control estándar de la mayoría de hostings colombianos) con **Python App** (Passenger/WSGI).

> ⚠️ **Requisito previo**: Tu plan de hosting debe soportar **Python** y tener acceso a **SSH** (Terminal). La mayoría de planes Hosting Business o superior lo incluyen. Verifica con tu proveedor antes de iniciar.

---

## 2. Paso 1 — Crear el Subdominio en cPanel

1. Ingresa a tu cPanel (normalmente en `https://educaciondigitalsena.com.co:2083`).
2. Ve a la sección **Dominios** → **Subdominios**.
3. En el campo **Subdominio**, escribe: `salas`
4. El campo **Dominio** debe mostrar: `educaciondigitalsena.com.co`
5. El campo **Raíz del documento** se llenará automáticamente: `public_html/salas`
6. Haz clic en **Crear**.

✅ Ya tienes: `salas.educaciondigitalsena.com.co` apuntando a `/public_html/salas/`

---

## 3. Paso 2 — Abrir la Terminal SSH

1. En cPanel, busca el ícono **Terminal** (o **SSH Access**).
2. Haz clic en **Abrir Terminal en el navegador**.
3. Si prefieres usar PuTTY, el host es `educaciondigitalsena.com.co` y el puerto es `22`.

---

## 4. Paso 3 — Subir el Código al Servidor

**Opción A (Recomendada): Por Git**
```bash
cd ~/public_html/salas
git clone https://github.com/edelgado-1975/Sala_de_juntas.git .
```

**Opción B: Por cPanel File Manager**
1. Comprime el proyecto en un `.zip` desde tu PC.
2. En cPanel → **Administrador de Archivos**, sube el `.zip` a `/public_html/salas/`.
3. Extrae el archivo ahí mismo.

---

## 5. Paso 4 — Crear el Entorno Python

En el cPanel busca **Aplicaciones de Python** (o "Setup Python App"):

1. Haz clic en **Create Application**.
2. Configura:
   - **Python version**: 3.12 o superior
   - **Application root**: `public_html/salas`
   - **Application URL**: `salas.educaciondigitalsena.com.co`
   - **Application startup file**: `passenger_wsgi.py` (lo crearemos en el Paso 6)
   - **Application Entry point**: `application`
3. Haz clic en **Create** y anota el comando de activación que te da cPanel, parecido a:
```bash
source /home/TU_USUARIO/virtualenv/public_html/salas/3.10/bin/activate
```

---

## 6. Paso 5 — Instalar Dependencias

En la terminal SSH, activa el entorno virtual con el comando del paso anterior, luego:
```bash
cd ~/public_html/salas
pip install -r requirements.txt
```

---

## 7. Paso 6 — Crear el Archivo `passenger_wsgi.py`

Este archivo es el puente entre el hosting y Django. Créalo en la raíz del proyecto:
```bash
nano ~/public_html/salas/passenger_wsgi.py
```

Pega exactamente este contenido (cambia `TU_USUARIO` por tu nombre de usuario en cPanel):
```python
import sys, os

# Ruta al entorno virtual
VENV_PATH = '/home/TU_USUARIO/virtualenv/public_html/salas/3.10/lib/python3.10/site-packages'

# Agregar paquetes del entorno virtual al path
if VENV_PATH not in sys.path:
    sys.path.insert(0, VENV_PATH)

# Agregar la raíz del proyecto al path
PROJECT_PATH = '/home/TU_USUARIO/public_html/salas'
if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salajuntas.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Guarda con `Ctrl+O`, `Enter`, luego `Ctrl+X`.

---

## 8. Paso 7 — Configurar el Archivo `.env`

```bash
nano ~/public_html/salas/.env
```

Pega la configuración de producción:
```env
SECRET_KEY=clave-secreta-muy-larga-y-aleatoria-para-produccion
DEBUG=False
ALLOWED_HOSTS=salas.educaciondigitalsena.com.co,www.salas.educaciondigitalsena.com.co

# Base de datos (crear en cPanel -> MySQL Databases)
DB_NAME=TU_USUARIO_salajuntas
DB_USER=TU_USUARIO_senauser
DB_PASSWORD=contraseña_segura
DB_HOST=localhost
DB_PORT=3306

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=contraseña_de_aplicacion_gmail
DEFAULT_FROM_EMAIL=SENA Sala de Juntas <tu_correo@gmail.com>
# Email que recibirá copia de todas las cancelaciones
ADMIN_EMAIL=tu_correo_admin@gmail.com
```

---

## 9. Paso 8 — Crear la Base de Datos MySQL en cPanel

1. En cPanel → **MySQL Databases (Bases de datos MySQL)**.
2. Crea una nueva base de datos: `TU_USUARIO_salajuntas`
3. Crea un usuario: `TU_USUARIO_senauser` con una contraseña segura.
4. Asigna **TODOS los privilegios** del usuario a la base de datos.
5. Usa esos mismos datos en el `.env` del paso anterior.

---

## 10. Paso 9 — Preparar la Aplicación

```bash
cd ~/public_html/salas
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

---

## 11. Paso 10 — Configurar Archivos Estáticos

Para que el hosting sirva los archivos CSS/JS, crea o edita el archivo `.htaccess` en `/public_html/salas/staticfiles/`:

```bash
nano ~/public_html/salas/staticfiles/.htaccess
```

Contenido:
```apache
Options -Indexes
<IfModule mod_headers.c>
    Header set Cache-Control "max-age=86400, public"
</IfModule>
```

También verifica que en `settings.py` el `STATIC_ROOT` apunte correctamente:
```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
```

---

## 12. Paso 11 — Reiniciar la Aplicación Python

En cPanel → **Aplicaciones de Python** → haz clic en el botón **Restart** junto a tu aplicación.

O desde la terminal:
```bash
touch ~/public_html/salas/tmp/restart.txt
```

---

## 13. Paso 12 — Activar HTTPS (SSL Gratuito)

1. En cPanel → **SSL/TLS** → **Certificados SSL de Let's Encrypt (AutoSSL)**.
2. Selecciona el subdominio `salas.educaciondigitalsena.com.co`.
3. Haz clic en **Instalar certificado**.

Espera unos minutos y tu aplicación estará disponible con HTTPS seguro en:
`https://salas.educaciondigitalsena.com.co` 🔒

---

## 14. Verificación Final

Abre el navegador y accede a:
`https://salas.educaciondigitalsena.com.co`

✅ Si ves la pantalla de login del sistema SENA, ¡el despliegue fue exitoso!

---

## 15. Actualizar el Código en el Futuro

Cuando hagas cambios y los subas a GitHub:
```bash
cd ~/public_html/salas
git pull origin main
python manage.py migrate
python manage.py collectstatic --noinput
touch tmp/restart.txt   # Reinicia la app
```

---

## 16. Solución de Problemas Comunes

| Problema | Solución |
|---|---|
| Error 500 al abrir la web | Revisar el log en cPanel → `Logs de errores`. Verificar `passenger_wsgi.py` y `.env`. |
| CSS/imágenes no cargan | Ejecutar `collectstatic` y revisar la ruta en `STATIC_ROOT`. |
| "Invalid HTTP_HOST header" | Agregar el dominio exacto a `ALLOWED_HOSTS` en el `.env`. |
| La app no reinicia tras cambios | Ejecutar `touch tmp/restart.txt` desde SSH. |
| Error de base de datos | Verificar credenciales en `.env` contra las de cPanel MySQL. |
