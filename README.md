# Sistema de Agendamiento de Sala de Juntas - SENA

Sistema web profesional para el control y agendamiento de salas de juntas del **SENA Centro de la Construcción, Cali**.

## 📋 Descripción

Aplicación web desarrollada en Django que permite gestionar las reservas de salas de juntas de forma eficiente, visualizar disponibilidad en tiempo real, generar informes y operar desde cualquier dispositivo (PC, tablet, móvil).

## ✨ Características Principales

- ✅ **Sistema de autenticación** completo (login, registro, recuperación de contraseña)
- ✅ **Calendario interactivo** para visualizar y crear reservas
- ✅ **Gestión de salas** con capacidades, equipamiento y horarios
- ✅ **Validación automática** de conflictos de horarios
- ✅ **Exportación a Google Calendar y Outlook** (formato .ics)
- ✅ **Informes y estadísticas** de ocupación
- ✅ **Diseño responsive** (funciona en móviles, tablets y PC)
- ✅ **Auditoría completa** de cambios en reservas
- ✅ **Roles de usuario** (Instructor, Administrativo, Coordinador)

## 🛠️ Tecnologías Utilizadas

- **Backend:** Django 6.0.2 + Python 3.13
- **Base de Datos:** MySQL 8.0+ (XAMPP)
- **Frontend:** HTML5, CSS3, JavaScript (FullCalendar.js)
- **Servidor Web:** Apache (XAMPP) con mod_wsgi

## 📦 Requisitos Previos

### Software Necesario

1. **Python 3.10 o superior**
   - Descargar desde: https://www.python.org/downloads/
   
2. **XAMPP para Windows**
   - Descargar desde: https://www.apachefriends.org/
   - Incluye MySQL y Apache
   
3. **Git** (para control de versiones)
   - Descargar desde: https://git-scm.com/

## 🚀 Instalación Paso a Paso

### Paso 1: Instalar y Configurar XAMPP

1. Instalar XAMPP
2. Abrir el XAMPP Control Panel
3. Iniciar los servicios **Apache** y **MySQL**
4. Abrir phpMyAdmin: http://localhost/phpmyadmin
5. Crear una nueva base de datos llamada `salajuntas_db`

### Paso 2: Clonar el Proyecto

```bash
cd d:\
git clone [URL-DEL-REPOSITORIO] SalaJuntasCC
cd SalaJuntasCC
```

### Paso 3: Crear Entorno Virtual

```powershell
python -m venv venv
venv\Scripts\activate
```

### Paso 4: Instalar Dependencias

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

**Nota:** Si `mysqlclient` falla al instalar, descarga el archivo .whl desde:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient

### Paso 5: Configurar Variables de Entorno

El proyecto ya incluye un archivo `.env` con configuración por defecto. Revisa y ajusta si es necesario:

- `DB_NAME`: salajuntas_db
- `DB_USER`: root  
- `DB_PASSWORD`: (vacío por defecto en XAMPP)
- `DB_HOST`: localhost
- `DB_PORT`: 3306

### Paso 6: Ejecutar Migraciones

```powershell
python manage.py makemigrations
python manage.py migrate
```

### Paso 7: Crear Superusuario

```powershell
python manage.py createsuperuser
```

Sigue las instrucciones y proporciona:
- Username (ejemplo: admin)
- Email
- Password
- Documento de identidad
- Otros campos opcionales

### Paso 8: Recolectar Archivos Estáticos

```powershell
python manage.py collectstatic
```

### Paso 9: Ejecutar el Servidor de Desarrollo

```powershell
python manage.py runserver
```

Accede a: **http://localhost:8000**

## 📱 Acceso desde Dispositivos Móviles (Red Local)

1. Obtén tu IP local de Windows:
   ```powershell
   ipconfig
   ```
   Busca la dirección IPv4 (ejemplo: 192.168.1.100)

2. En tu `.env`, actualiza:
   ```
   ALLOWED_HOSTS=localhost,127.0.0.1,192.168.1.100
   ```

3. Ejecuta el servidor especificando la IP:
   ```powershell
   python manage.py runserver 0.0.0.0:8000
   ```

4. Desde tu móvil, accede a: `http://192.168.1.100:8000`

## 📂 Estructura del Proyecto

```
SalaJuntasCC/
├── apps/
│   ├── usuarios/       # Autenticación y gestión de usuarios
│   ├── salas/          # Gestión de salas de juntas
│   ├── reservas/       # Sistema de agendamiento
│   └── informes/       # Reportes y estadísticas
├── salajuntas/         # Configuración principal del proyecto
├── static/             # CSS, JavaScript, imágenes
├── templates/          # Plantillas HTML
├── media/              # Archivos subidos por usuarios
├── docs/               # Documentación del proyecto
├── deployment/         # Archivos de configuración para despliegue
├── requirements.txt    # Dependencias Python
├── .env                # Variables de entorno (NO subir a Git)
├── .gitignore          # Archivos excluidos de Git
└── manage.py           # Comandos de gestión Django
```

## 📚 Documentación Adicional

- **Manual de Usuario:** Ver `docs/MANUAL_USUARIO.md`
- **Manual de Despliegue:** Ver `docs/MANUAL_DESPLIEGUE.md`
- **Guía de GitHub:** Ver `docs/GUIA_GITHUB.md`

## 🔐 Panel de Administración

Accede al panel de administración en: **http://localhost:8000/admin**

Desde aquí puedes:
- Gestionar usuarios
- Crear y editar salas
- Ver todas las reservas
- Acceder a estadísticas

## 🤝 Contribución y Versionado

Este proyecto utiliza Git para control de versiones. Para contribuir:

1. Crea una rama para tu funcionalidad: `git checkout -b feature/nueva-funcionalidad`
2. Realiza tus cambios y commits descriptivos
3. Push a GitHub: `git push origin feature/nueva-funcionalidad`
4. Crea un Pull Request

Ver `docs/GUIA_GITHUB.md` para instrucciones detalladas.

## 📄 Licencia

Este proyecto es de uso interno del SENA Centro de la Construcción, Cali.

## 📧 Contacto y Soporte

Para soporte o consultas sobre el sistema:
- Email: soporte@sena.edu.co
- Centro: SENA - Centro de la Construcción
- Ciudad: Cali, Colombia

---

**Desarrollado con ❤️ para el SENA Centro de la Construcción**
