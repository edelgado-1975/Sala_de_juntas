# ⚙️ Manual de Despliegue e Instalación
## Sistema de Agendamiento de Salas de Juntas - SENA
**Centro de la Construcción, Cali | Versión 1.0.0 | Febrero 2026**

---

## 1. Requisitos del Sistema

### Servidor
- **Sistema Operativo**: Windows Server 2019+ o Ubuntu 20.04+
- **RAM**: Mínimo 2 GB (recomendado 4 GB)
- **Almacenamiento**: Mínimo 10 GB libres
- **Acceso a red**: Puerto 80 (HTTP) y 443 (HTTPS) abiertos

### Software Requerido
| Software | Versión Mínima |
|---|---|
| Python | 3.10 |
| MySQL | 8.0 |
| Git | 2.x |
| pip | 23.x |

---

## 2. Instalación en Entorno Local (Desarrollo)

### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/edelgado-1975/Sala_de_juntas.git
cd Sala_de_juntas
```

### Paso 2: Crear y Activar Entorno Virtual
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Base de Datos MySQL
1. Crear la base de datos en MySQL:
```sql
CREATE DATABASE sala_juntas_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'sena_user'@'localhost' IDENTIFIED BY 'tu_contraseña_segura';
GRANT ALL PRIVILEGES ON sala_juntas_db.* TO 'sena_user'@'localhost';
FLUSH PRIVILEGES;
```

2. Configurar las credenciales en `salajuntas/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sala_juntas_db',
        'USER': 'sena_user',
        'PASSWORD': 'tu_contraseña_segura',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Paso 5: Aplicar Migraciones
```bash
python manage.py migrate
```

### Paso 6: Crear Super Usuario Administrador
```bash
python manage.py createsuperuser
```
Sigue las instrucciones e ingresa nombre de usuario, email y contraseña.

### Paso 7: Iniciar el Servidor de Desarrollo
```bash
python manage.py runserver 0.0.0.0:8000
```
Accede a `http://localhost:8000` en tu navegador.

---

## 3. Despliegue en Producción (Servidor Real)

> ⚠️ **IMPORTANTE**: Para producción, nunca usar `runserver`. Usar Gunicorn + Nginx.

### Paso 1: Configurar Variables de Entorno
Crear un archivo `.env` en la raíz del proyecto (nunca subir a Git):
```env
SECRET_KEY=tu_clave_secreta_muy_larga_y_aleatoria
DEBUG=False
ALLOWED_HOSTS=tu_dominio.com,www.tu_dominio.com
DB_NAME=sala_juntas_db
DB_USER=sena_user
DB_PASSWORD=tu_contraseña_segura
DB_HOST=localhost
```

### Paso 2: Instalar Gunicorn
```bash
pip install gunicorn
```

### Paso 3: Recolectar Archivos Estáticos
```bash
python manage.py collectstatic --noinput
```

### Paso 4: Configurar Gunicorn como Servicio (Linux)
Crear el archivo `/etc/systemd/system/salajuntas.service`:
```ini
[Unit]
Description=Sala Juntas SENA - Gunicorn
After=network.target

[Service]
User=www-data
WorkingDirectory=/ruta/al/proyecto
ExecStart=/ruta/al/venv/bin/gunicorn --workers 3 --bind unix:/run/salajuntas.sock salajuntas.wsgi:application

[Install]
WantedBy=multi-user.target
```

Activar el servicio:
```bash
sudo systemctl enable salajuntas
sudo systemctl start salajuntas
```

### Paso 5: Configurar Nginx como Proxy Inverso
Crear `/etc/nginx/sites-available/salajuntas`:
```nginx
server {
    listen 80;
    server_name tu_dominio.com;

    location /static/ {
        alias /ruta/al/proyecto/staticfiles/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/salajuntas.sock;
    }
}
```

Activar la configuración:
```bash
sudo ln -s /etc/nginx/sites-available/salajuntas /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

---

## 4. Verificación Post-Despliegue

Después de instalar, verificar que todo funcione:

- [ ] La página de login carga correctamente.
- [ ] Se puede iniciar sesión con el Super Usuario.
- [ ] El calendario muestra los eventos correctamente.
- [ ] Se puede crear una reserva sin errores.
- [ ] Los informes se generan y exportan.
- [ ] El panel de administración (`/admin`) es accesible.

---

## 5. Actualización del Sistema

Para aplicar una nueva versión del código:
```bash
git pull origin main
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart salajuntas
```

---

## 6. Información del Repositorio

- **GitHub**: https://github.com/edelgado-1975/Sala_de_juntas
- **Versión**: v1.0.0
- **Fecha de Lanzamiento**: Febrero 2026
