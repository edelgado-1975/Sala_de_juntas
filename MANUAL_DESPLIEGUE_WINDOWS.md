# ⚙️ Manual de Despliegue en Windows Server
## Sistema de Agendamiento de Salas de Juntas - SENA
**Centro de la Construcción, Cali | Versión 1.0.0 | Febrero 2026**

---

## 1. Requisitos del Sistema (Windows)

| Componente | Versión Recomendada | Descarga |
|---|---|---|
| Windows Server | 2019 / 2022 | — |
| Python | 3.10 o superior | python.org |
| MySQL | 8.0 | mysql.com |
| Git | 2.x | git-scm.com |
| waitress | (se instala con pip) | — |

> 💡 **¿Por qué `waitress`?** En Windows no se puede usar Gunicorn (solo funciona en Linux). `waitress` es su equivalente para Windows, igualmente robusto.

---

## 2. Paso 1 — Instalar Python

1. Descarga el instalador desde `https://www.python.org/downloads/`
2. Al instalar, **marca** la opción `☑ Add Python to PATH`.
3. Verifica la instalación:
```powershell
python --version
```

---

## 3. Paso 2 — Instalar MySQL

1. Descarga MySQL Community Server desde `https://dev.mysql.com/downloads/mysql/`
2. Durante la instalación, anota la contraseña del usuario `root`.
3. Crea la base de datos de producción:
```sql
CREATE DATABASE salajuntas_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'sena_user'@'localhost' IDENTIFIED BY 'CambiaEstaPorUnaSegura123!';
GRANT ALL PRIVILEGES ON salajuntas_prod.* TO 'sena_user'@'localhost';
FLUSH PRIVILEGES;
```

---

## 4. Paso 3 — Clonar el Proyecto

Abre PowerShell como Administrador:
```powershell
cd C:\
git clone https://github.com/edelgado-1975/Sala_de_juntas.git
cd Sala_de_juntas
```

---

## 5. Paso 4 — Crear Entorno Virtual e Instalar Dependencias

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
pip install waitress    # Servidor de producción para Windows
```

---

## 6. Paso 5 — Configurar el Archivo `.env`

Crea o edita el archivo `C:\Sala_de_juntas\.env`:
```env
SECRET_KEY=una-clave-secreta-muy-larga-y-aleatoria-aqui
DEBUG=False
ALLOWED_HOSTS=tu-ip-del-servidor,localhost,127.0.0.1

DB_NAME=salajuntas_prod
DB_USER=sena_user
DB_PASSWORD=CambiaEstaPorUnaSegura123!
DB_HOST=localhost
DB_PORT=3306

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=tu_contrasena_de_aplicacion
DEFAULT_FROM_EMAIL=SENA Sala de Juntas <tu_correo@gmail.com>
```

---

## 7. Paso 6 — Preparar la Aplicación

```powershell
# Aplicar migraciones a la base de datos
python manage.py migrate

# Recolectar archivos estáticos (CSS, JS, imágenes)
python manage.py collectstatic --noinput

# Crear el administrador del sistema
python manage.py createsuperuser
```

---

## 8. Paso 7 — Iniciar el Servidor con Waitress

```powershell
waitress-serve --host=0.0.0.0 --port=8000 salajuntas.wsgi:application
```

La aplicación estará disponible en `http://IP_DEL_SERVIDOR:8000`.

---

## 9. Paso 8 — Ejecutar como Servicio de Windows (Inicio Automático)

Para que el servidor inicie automáticamente con Windows, instala `NSSM`:

1. Descarga NSSM desde `https://nssm.cc/download`
2. Extrae `nssm.exe` a `C:\Windows\System32`
3. Abre PowerShell como Administrador y ejecuta:

```powershell
nssm install SalaJuntasSENA
```

4. En el formulario que aparece, configura:
   - **Path**: `C:\Sala_de_juntas\venv\Scripts\waitress-serve.exe`
   - **Arguments**: `--host=0.0.0.0 --port=8000 salajuntas.wsgi:application`
   - **Startup directory**: `C:\Sala_de_juntas`

5. Haz clic en **Install service** y luego:
```powershell
nssm start SalaJuntasSENA
```

---

## 10. Paso 9 — Abrir Puerto en el Firewall de Windows

```powershell
netsh advfirewall firewall add rule name="Sala Juntas SENA" dir=in action=allow protocol=TCP localport=8000
```

---

## 11. Verificación Final

Abre un navegador en otro computador de la red y accede a:
`http://IP_DEL_SERVIDOR:8000`

✅ Si ves la pantalla de login del sistema, ¡el despliegue fue exitoso!

---

## 12. Comandos de Mantenimiento

| Acción | Comando |
|---|---|
| Iniciar servicio | `nssm start SalaJuntasSENA` |
| Detener servicio | `nssm stop SalaJuntasSENA` |
| Reiniciar tras actualización | `nssm restart SalaJuntasSENA` |
| Ver logs | `nssm status SalaJuntasSENA` |

Para actualizar el código:
```powershell
cd C:\Sala_de_juntas
git pull origin main
.\venv\Scripts\activate
python manage.py migrate
python manage.py collectstatic --noinput
nssm restart SalaJuntasSENA
```
