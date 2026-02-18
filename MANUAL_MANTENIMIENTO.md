# 🔧 Manual de Mantenimiento
## Sistema de Agendamiento de Salas de Juntas - SENA
**Centro de la Construcción, Cali | Versión 1.0.0 | Febrero 2026**

---

## 1. Arquitectura del Sistema

```
SalaJuntasCC/
├── apps/
│   ├── informes/       # Módulo de reportes y estadísticas
│   ├── reservas/       # Módulo principal de agendamiento
│   └── usuarios/       # Módulo de autenticación y roles
├── salajuntas/         # Configuración principal de Django
├── static/             # Archivos estáticos (CSS, JS, imágenes)
├── templates/          # Plantillas HTML
├── manage.py
└── requirements.txt
```

**Stack Tecnológico:**
- **Backend**: Python 3.10+, Django 5.0
- **Base de Datos**: MySQL 8.0
- **Frontend**: Bootstrap 5, FullCalendar 6, JavaScript
- **Control de Versiones**: Git + GitHub

---

## 2. Tareas de Mantenimiento Rutinario

### 2.1 Copias de Seguridad (Diario)
Ejecutar el siguiente comando para respaldar la base de datos MySQL:
```bash
mysqldump -u root -p sala_juntas_db > backup_$(date +%Y%m%d).sql
```
Guardar los backups en una ubicación externa o en la nube.

### 2.2 Limpieza de Reservas Antiguas (Mensual)
Desde el panel de administración Django (`/admin`), filtrar y eliminar reservas canceladas con más de 6 meses de antigüedad para mantener la base de datos liviana.

### 2.3 Actualización de Dependencias (Trimestral)
```bash
# Activar entorno virtual
.\venv\Scripts\activate

# Ver dependencias desactualizadas
pip list --outdated

# Actualizar una dependencia específica (con precaución)
pip install --upgrade nombre_paquete

# Guardar el nuevo estado
pip freeze > requirements.txt
```
> ⚠️ **Siempre probar en un entorno de desarrollo antes de actualizar en producción.**

### 2.4 Rotación de Logs (Mensual)
Los logs del servidor se acumulan en la carpeta de logs de Django. Revisar y archivar mensualmente.

---

## 3. Gestión de Usuarios desde el Panel Admin

1. Acceder a `http://servidor/admin` con credenciales de Super Usuario.
2. Ir a **Usuarios** → **Usuarios**.
3. Para cambiar el rol de un usuario:
   - Seleccionar el usuario.
   - Modificar el campo **Tipo de Usuario** (Consulta / Operativo / Super Usuario).
   - Guardar cambios.

---

## 4. Gestión de Salas

1. Desde el menú principal, ir a **Admin** → **Salas**.
2. Aquí puedes:
   - **Crear** nuevas salas con nombre, capacidad y descripción.
   - **Editar** la información de salas existentes.
   - **Desactivar** una sala (sin eliminarla) para que no aparezca en el calendario.

---

## 5. Reglas de Calidad - Parámetros Configurables

Los siguientes parámetros están definidos en `apps/reservas/forms.py` y pueden ajustarse según las políticas del centro:

| Parámetro | Valor Actual | Ubicación en Código |
|---|---|---|
| Hora mínima de operación | 7:00 AM | `fecha_inicio.hour < 7` |
| Hora máxima de operación | 9:30 PM | `fecha_inicio.hour > 21` |
| Buffer entre reuniones | 15 minutos | `timedelta(minutes=15)` |
| Anticipación mínima | 1 hora | `timedelta(hours=1)` |
| Anticipación máxima | 90 días | `timedelta(days=90)` |
| Mínimo de ocupación | 10% capacidad | `sala.capacidad * 0.1` |

---

## 6. Actualización de Código desde GitHub

Para aplicar actualizaciones del repositorio en el servidor:
```bash
# 1. Ir a la carpeta del proyecto
cd /ruta/al/proyecto

# 2. Descargar los últimos cambios
git pull origin main

# 3. Aplicar migraciones si hay cambios en modelos
python manage.py migrate

# 4. Recolectar archivos estáticos
python manage.py collectstatic --noinput

# 5. Reiniciar el servidor web (ej: Gunicorn)
sudo systemctl restart gunicorn
```

---

## 7. Solución de Problemas Comunes

| Problema | Causa Probable | Solución |
|---|---|---|
| El calendario no carga | Error en la API de eventos | Revisar logs del servidor. Verificar conexión a BD. |
| No se puede guardar una reserva | Error de validación o BD | Revisar los mensajes de error en el formulario. |
| El logo SENA no aparece | Archivos estáticos no servidos | Ejecutar `python manage.py collectstatic`. |
| Error 500 en producción | Error interno del servidor | Revisar `DEBUG=False` y los logs de error de Django. |
| Usuario no puede iniciar sesión | Contraseña incorrecta o cuenta inactiva | Verificar en el panel Admin que el usuario esté activo. |

---

## 8. Contacto y Soporte

- **Repositorio**: https://github.com/edelgado-1975/Sala_de_juntas
- **Versión**: v1.0.0
- **Fecha**: Febrero 2026
