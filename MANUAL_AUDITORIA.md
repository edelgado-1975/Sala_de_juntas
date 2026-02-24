# 📋 Manual de Procedimientos para Auditoría de Sistemas
## Proyecto: Sistema de Agendamiento de Salas de Juntas - SENA v1.1.0

Este documento define los protocolos oficiales para auditar la **Seguridad**, **Integridad** y **Transparencia** del sistema, garantizando el cumplimiento continuo de la norma **ISO/IEC 25000 (SQuaRE)**.

---

## 1. Objetivos de la Auditoría
*   **Garantizar la Trazabilidad**: Identificar quién, cuándo y qué se modificó en el sistema.
*   **Asegurar la Disponibilidad**: Verificar que los servicios de base de datos y correo operen correctamente.
*   **Protección de Datos**: Validar la integridad de la información institucional del SENA.
*   **Seguridad Activa**: Detectar y mitigar intentos de acceso no autorizados.

---

## 2. Protocolos de Auditoría Técnica

### 2.1 Auditoría de Seguridad de Acceso
**Frecuencia**: Semanal.
**Procedimiento**:
1.  Acceder al Panel Administrativo (`/admin`).
2.  Navegar al módulo **Usuarios** -> **Logs de Seguridad**.
3.  Revisar registros de "Login Fallido".
    *   *Umbral Crítico*: Más de 5 intentos fallidos desde una misma IP en una hora.
4.  Verificar usuarios inactivos que aún tengan permisos de Operativo.

### 2.2 Auditoría de Operatividad y Reservas
**Frecuencia**: Diaria (Automatizada) / Quincenal (Manual).
**Procedimiento**:
1.  Verificar el log de notificaciones por correo.
2.  Revisar el módulo **Reservas** -> **Historial de Auditoría** (Signals).
3.  Validar que no existan reservas en estado "Confirmada" que violen las reglas de negocio (Lead times o Buffers).
4.  Comprobar la coherencia entre el aforo de la sala y la reserva realizada.

### 2.3 Auditoría de Integridad de Datos
**Frecuencia**: Mensual.
**Procedimiento**:
1.  Validar la existencia y consistencia de los Backups en MySQL.
2.  Ejecutar el comando de verificación de base de datos:
    ```powershell
    python manage.py check 
    ```
3.  Revisar el **Diccionario de Datos** para asegurar que no existan campos vacíos críticos en las tablas de `usuarios_perfil`.

---

## 3. Matriz de Frecuencia y Responsabilidades

| Tipo de Auditoría | Frecuencia | Responsable | Entregable |
| :--- | :--- | :--- | :--- |
| **Seguridad Login** | Semanal | Administrador TI | Reporte de Accesos |
| **Trazabilidad de Reservas** | Diaria | Operativo Líder | Bitácora de Cambios |
| **Desempeño del Sistema** | Semanal | Mantenimiento | Log de Velocidad |
| **Integridad de Base de Datos** | Mensual | Admin Base Datos | Acta de Backup |
| **Cumplimiento ISO 25000** | Semestral | Comité de Calidad | Informe de Calidad |

---

## 4. Herramientas de Auditoría Incorporadas

El sistema v1.1.0 incluye herramientas nativas para facilitar este proceso:
*   **Logs de Django Signals**: Registro automático de toda acción de creación, edición o borrado.
*   **Security Logs**: Interfaz para visualizar intentos de fuerza bruta.
*   **Email Logs**: Auditoría de entrega de notificaciones institucionales.
*   **Dashboard de Informes**: Generación de estadísticas de uso y ocupación en tiempo real.

---

## 5. Protocolo de Hallazgos y Acciones Correctivas

1.  **Identificación**: Se registra la anomalía detectada.
2.  **Clasificación**: Se define como *Leve*, *Moderada* o *Crítica* según la matriz de riesgos ISO 25000.
3.  **Resolución**: Se aplica el ajuste técnico (ej: cambio de contraseña, bloqueo de IP, restauración de Backup).
4.  **Cierre**: Se documenta la acción tomada en el Manual de Mantenimiento.

---
**Documento Generado el**: 24 de Febrero de 2026
**Estatus**: v1.1.0 - Calidad y Transparencia
**Responsable**: Antigravity AI
