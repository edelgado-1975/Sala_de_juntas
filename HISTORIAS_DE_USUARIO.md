# 📋 Historias de Usuario (ISO/IEC 25000)
## Proyecto: Sistema de Agendamiento de Salas de Juntas - SENA v1.0.0

Este documento detalla los requerimientos funcionales y no funcionales del sistema bajo el estándar **ISO/IEC 25000**, asegurando que cada funcionalidad cumpla con los atributos de calidad de producto de software (SQuaRE).

---

## 🏛️ Módulo 1: Gestión de Identidad y Acceso (Seguridad)

### HU01: Inicio de Sesión Seguro
**Como** Usuario del SENA (Administrador/Operativo/Consulta),
**Quiero** autenticarme en el sistema mediante mis credenciales,
**Para** acceder a las funciones permitidas según mi rol institucional.

**Criterios de Aceptación:**
1. El sistema debe validar que las credenciales existan en la base de datos MySQL.
2. Tras 5 intentos fallidos, el sistema debe registrar un log de advertencia (Seguridad).
3. La sesión debe expirar tras 300 segundos de inactividad (Fiabilidad).

**Atributos de Calidad ISO 25000:**
- **Seguridad**: Autenticación y control de acceso.
- **Fiabilidad**: Madurez en la persistencia de sesión.

---

## 📅 Módulo 2: Agendamiento y Calendario (Adecuación Funcional)

### HU02: Creación de Reserva en Calendario
**Como** Funcionario SENA,
**Quiero** seleccionar un espacio de tiempo en el calendario visual,
**Para** agendar una sala de juntas para mis actividades.

**Criterios de Aceptación:**
1. El usuario debe ver la disponibilidad en tiempo real mediante FullCalendar.
2. El sistema debe permitir ingresar: Sala, Propósito, Fecha de Inicio y Fin.
3. El sistema debe asignar automáticamente el color institucional según el estado.

**Atributos de Calidad ISO 25000:**
- **Adecuación Funcional**: Pertinencia de las tareas.
- **Usabilidad**: Estética de la interfaz y facilidad de aprendizaje.

### HU03: Validación Anti-Solapamiento (Calidad QA)
**Como** Sistema de Gestión,
**Quiero** verificar que no existan cruces de horarios,
**Para** evitar conflictos en el uso de los espacios físicos.

**Criterios de Aceptación:**
1. El sistema debe rechazar cualquier reserva que interfiera con una existente.
2. Se debe respetar un buffer de 15 minutos entre sesiones consecutivas.
3. El agendamiento debe realizarse con al menos 1 hora de anticipación.

**Atributos de Calidad ISO 25000:**
- **Fiabilidad**: Tolerancia a fallos de usuario.
- **Adecuación Funcional**: Corrección funcional (Exactitud).

---

## 📧 Módulo 3: Notificaciones e Integración (Interoperabilidad)

### HU04: Notificación Automática de Cancelación
**Como** Administrador del Sistema,
**Quiero** que el sistema notifique al usuario vía email cuando su reserva sea cancelada,
**Para** mantener la transparencia en la comunicación institucional.

**Criterios de Aceptación:**
1. El disparo del email debe realizarse mediante Signals de Django (independiente de la vista).
2. Se deben enviar correos individuales para asegurar la entrega.
3. El correo debe contener los detalles exactos de la reserva afectada.

**Atributos de Calidad ISO 25000:**
- **Compatibilidad**: Interoperabilidad con servidores SMTP externos.
- **Fiabilidad**: Capacidad de recuperación (logs de envío).

---

## 📊 Módulo 4: Informes y Auditoría (Mantenibilidad)

### HU05: Generación de Reportes de Ocupación
**Como** Usuario Operativo/Administrador,
**Quiero** generar estadísticas de uso de las salas,
**Para** analizar la eficiencia en la utilización de los recursos del Centro.

**Criterios de Aceptación:**
1. El sistema debe permitir filtrar por rango de fechas y sala específica.
2. Los reportes deben ser exportables a formato PDF y Excel (.csv).
3. El tiempo de generación del reporte debe ser inferior a 2 segundos (Desempeño).

**Atributos de Calidad ISO 25000:**
- **Eficiencia de Desempeño**: Comportamiento temporal.
- **Mantenibilidad**: Modularidad del sistema de informes.

---

## 📱 Módulo 5: Experiencia Multidispositivo (Portabilidad)

### HU06: Operación desde Dispositivos Móviles
**Como** Usuario Móvil (Android/iOS),
**Quiero** visualizar y gestionar mis reservas desde mi celular,
**Para** operar el sistema fuera de la oficina.

**Criterios de Aceptación:**
1. La interfaz debe adaptarse automáticamente mediante RWD (Responsive Web Design).
2. Los botones y modales deben tener un tamaño mínimo "táctil" (44px).
3. El menú principal debe ocultarse en un componente lateral (Drawer/Offcanvas).

**Atributos de Calidad ISO 25000:**
- **Portabilidad**: Adaptabilidad a diferentes plataformas.
- **Usabilidad**: Operatividad multicanal.

---
**Documento Generado el**: 24 de Febrero de 2026
**Responsable de Documentación**: Antigravity AI
