# 🧪 Plan de Pruebas Propuesto
## Sistema de Agendamiento de Salas de Juntas - SENA
**Centro de la Construcción, Cali | Versión 1.0.0 | Febrero 2026**

---

## 1. Introducción
El objetivo de este plan es garantizar la integridad, seguridad y calidad del sistema antes de su puesta en marcha oficial. Se dividirá en tres niveles: Pruebas Funcionales (Manuales), Pruebas de Calidad (Reglas de Negocio) y Pruebas de Seguridad (Roles).

---

## 2. Nivel 1: Pruebas Funcionales (Checklist Manual)

| Módulo | Escenario de Prueba | Resultado Esperado |
|---|---|---|
| **Acceso** | Login con credenciales válidas e inválidas. | Acceso permitido solo con datos correctos. |
| **Perfil** | Subida de foto y edición de datos personales. | La información se actualiza y la foto se visualiza. |
| **Calendario** | Navegación entre meses y vistas (Lista/Mes). | Los eventos se cargan correctamente según el filtro. |
| **Reservas** | Crear una reserva desde el modal del calendario. | El evento aparece en el calendario inmediatamente. |
| **Informes** | Generación de reporte por usuario/sala en PDF. | El PDF se descarga con la información filtrada. |

---

## 3. Nivel 2: Verificación de Directivas de Calidad (Crítico)

Estas pruebas validan que las reglas institucionales del SENA se cumplan estrictamente:

| Regla de Calidad | Prueba a Realizar | Comportamiento Esperado |
|---|---|---|
| **Horario de Operación** | Intentar reservar a las 6:30 AM o 10:00 PM. | Bloqueo por horario (Sólo 7:00 AM - 9:30 PM). |
| **Anticipación Mínima** | Intentar reservar para dentro de los próximos 30 min. | Error: Se requiere mínimo 1 hora de anticipación. |
| **Buffer de Tiempo** | Intentar reservar sala X 15 min después de una cita. | Error: Debe existir un margen de 15 min entre reservas. |
| **Solapamientos** | Intentar reservar en un horario ya ocupado. | El sistema impide el guardado detectando el conflicto. |
| **Capacidad Mínima** | Intentar reservar sala de 20 pax para 1 persona. | Advertencia de sub-utilización de espacio. |

---

## 4. Nivel 3: Pruebas de Seguridad y Roles (RBAC)

Validar que cada usuario solo vea y haga lo que le corresponde:

| Rol | Prueba | Resultado Esperado |
|---|---|---|
| **Consulta** | Intentar crear una reserva. | Botón "Nueva Reserva" oculto o prohibición al guardar. |
| **Operativo** | Intentar editar la sala creada por otro usuario. | Botones de edición ocultos para registros ajenos. |
| **SuperUsuario** | Editar cualquier reserva de cualquier instructor. | Acceso total a edición y eliminación. |
| **Administración** | Acceso al panel `/admin`. | Solo el SuperUsuario puede ingresar a la configuración base. |

---

## 5. Nivel 4: Pruebas Técnicas (Próximos Pasos)

Para una automatización completa, se recomienda implementar los siguientes scripts en Python:

### A. Pruebas Unitarias (`tests.py`)
- Verificar que el modelo `Reserva` guarde los datos correctamente.
- Verificar que el cálculo de `duración` sea exacto.

### B. Pruebas de Carga
- Simular 50 usuarios consultando el calendario simultáneamente (usando herramientas como *Locust*).

---

## 6. Firma y Aprobación
Este plan debe ser ejecutado por el equipo operativo antes de la inauguración del servicio.

**Fecha de Ejecución Propuesta:** 24 de Febrero de 2026.
**Responsable:** Administrador del Sistema.
