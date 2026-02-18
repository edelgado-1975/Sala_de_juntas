# 📘 Manual de Usuario
## Sistema de Agendamiento de Salas de Juntas - SENA
**Centro de la Construcción, Cali | Versión 1.0.0 | Febrero 2026**

---

## 1. Introducción

Este sistema permite a los funcionarios y aprendices del SENA **reservar, gestionar y consultar** el uso de las salas de juntas de manera organizada y sin conflictos de horario.

---

## 2. Acceso al Sistema

### 2.1 Iniciar Sesión
1. Abre tu navegador y ve a la dirección del sistema (ej: `http://localhost:8000`).
2. Ingresa tu **correo electrónico** y **contraseña**.
3. Haz clic en **Iniciar Sesión**.

### 2.2 Registrarse (Nuevo Usuario)
1. En la pantalla de login, haz clic en **Registrarse**.
2. Completa el formulario con tus datos.
3. Tu cuenta iniciará con rol de **Consulta** (solo lectura). Un administrador deberá habilitarte para crear reservas.

### 2.3 Recuperar Contraseña
1. Haz clic en **¿Olvidaste tu contraseña?** en la pantalla de login.
2. Ingresa tu correo y sigue las instrucciones enviadas a tu email.

---

## 3. Roles de Usuario

| Rol | Descripción |
|---|---|
| 🔴 **Super Usuario** | Administración total: salas, usuarios y todas las reservas. |
| 🟡 **Operativo** | Puede crear, editar y cancelar sus propias reservas. |
| 🟢 **Consulta** | Solo puede ver el calendario. No puede crear reservas. |

---

## 4. Crear una Reserva

1. En el **Dashboard (Calendario)**, haz clic en el botón **➕ Nueva Reserva**.
2. Completa el formulario:
   - **Sala**: Selecciona la sala disponible.
   - **Fecha Inicio / Fecha Fin**: Elige el rango de tiempo.
   - **Propósito**: Describe brevemente el motivo de la reunión.
   - **Número de Asistentes**: Cuántas personas asistirán.
   - **Estado**: Por defecto es **Confirmada**.
3. Haz clic en **Guardar Reserva**.

### ⚠️ Reglas de Calidad (el sistema las valida automáticamente)
- Solo se puede reservar entre **7:00 AM y 9:30 PM**.
- Se requiere mínimo **1 hora de anticipación**.
- No se puede reservar con más de **90 días de antelación**.
- Debe haber un **margen de 15 minutos** entre reuniones en la misma sala.
- El número de asistentes debe ser coherente con la capacidad de la sala.

---

## 5. Ver y Filtrar el Calendario

- **Filtrar por Sala**: Selecciona una sala específica en el panel izquierdo y haz clic en **Filtrar**.
- **Filtrar por Estado**: Muestra solo reservas Confirmadas, Pendientes o Canceladas.
- **Vistas**: Cambia entre vista **Mes**, **Semana** o **Agenda** con los botones superiores.

### Código de Colores
| Color | Significado |
|---|---|
| 🔵 Azul | Mis propias reservas |
| 🟢 Verde | Reservas confirmadas de otros |
| 🟡 Amarillo | Reservas pendientes |
| 🔴 Rojo | Reservas canceladas |

---

## 6. Editar o Cancelar una Reserva

1. Haz clic sobre el evento en el calendario.
2. En el modal de detalles, haz clic en **✏️ Editar**.
3. Modifica los campos necesarios (incluyendo el **Estado** si deseas cancelarla).
4. Haz clic en **Guardar Cambios**.

> **Nota**: Solo puedes editar tus propias reservas. Los Super Usuarios pueden editar cualquiera.

---

## 7. Exportar una Reserva al Calendario Personal

En el modal de detalles de una reserva, encontrarás dos botones:
- **📅 Google Calendar**: Abre Google Calendar con los datos prellenados.
- **📆 Outlook (.ics)**: Descarga un archivo `.ics` para importar en Outlook o cualquier cliente de calendario.

---

## 8. Informes y Reportes

> Solo disponible para usuarios **Operativo** y **Super Usuario**.

1. En el menú superior, haz clic en **📊 Informes**.
2. Selecciona el tipo de informe:
   - **Ocupación por Sala**: Estadísticas de uso de cada sala.
   - **Por Usuario**: Historial de reservas de un usuario específico.
3. Aplica filtros de fecha y haz clic en **Generar Informe**.
4. Exporta el resultado a **PDF** o **Excel** con los botones correspondientes.

---

## 9. Gestión de Perfil

1. Haz clic en tu nombre en la esquina superior derecha.
2. Selecciona **Mi Perfil**.
3. Actualiza tu información personal o cambia tu contraseña.

---

## 10. Preguntas Frecuentes (FAQ)

**¿Por qué no puedo crear reservas?**
Tu cuenta tiene rol de **Consulta**. Contacta al administrador para que te asigne el rol **Operativo**.

**¿Por qué el sistema rechaza mi horario?**
Puede ser por solapamiento con otra reserva, horario fuera del rango permitido, o anticipación insuficiente. Lee el mensaje de error para más detalles.

**¿Puedo reservar para otra persona?**
Sí, si tienes rol **Operativo** o **Super Usuario** puedes crear reservas en nombre de otros.

---

*Para soporte técnico, contacta al administrador del sistema.*
