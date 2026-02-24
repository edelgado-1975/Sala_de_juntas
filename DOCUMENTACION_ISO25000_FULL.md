# 📖 Documentación de Calidad ISO/IEC 25000 (SQuaRE)
## Proyecto: Sistema de Agendamiento de Salas de Juntas - SENA v1.1.0

Esta documentación detalla los atributos de calidad del software implementados bajo el estándar internacional **ISO/IEC 25000**, adaptado para el contexto del Centro de la Construcción de la ciudad de Cali.

---

## 1. Adecuación Funcional (Functional Suitability)
Mide el grado en que el software proporciona funciones que satisfacen las necesidades declaradas e implícitas.

*   **Completitud Funcional**: El sistema cubre el ciclo total de agendamiento: Registro, Gestión de Salas, Reservas (Creación/Edición/Cancelación) e Informes.
*   **Corrección Funcional**: Se implementaron validaciones estrictas (`models.py` y `forms.py`) que aseguran que los datos procesados sean precisos (ej. validación de fechas, anticipación y buffers).
*   **Pertinencia Funcional**: Las funciones están alineadas con la operatividad del SENA, incluyendo reportes de ocupación y exportación de agendas.

---

## 2. Eficiencia de Desempeño (Performance Efficiency)
Evalúa el desempeño relativo a los recursos utilizados.

*   **Comportamiento Temporal**: Uso de `select_related` y `prefetch_related` en las consultas de Django para minimizar las peticiones a la base de datos MySQL, garantizando tiempos de respuesta sub-segundos en el calendario principal.
*   **Utilización de Recursos**: El sistema está optimizado para ejecutarse en entornos con recursos limitados (ej. servidores locales XAMPP) gracias a su arquitectura ligera.
*   **Capacidad**: Capacidad de manejar múltiples peticiones concurrentes mediante el servidor WSGI/ASGI de Django.

---

## 3. Compatibilidad (Compatibility)
Capacidad de intercambio de información y ejecución en un entorno compartido.

*   **Coexistencia**: Puede ejecutarse junto a otros servicios en un servidor Windows/Linux sin conflictos de puertos o dependencias mediante el uso de entornos virtuales (`venv`).
*   **Interoperabilidad**: Soporte para formatos estándares de la industria como `.ics` (Google Calendar / Outlook) y exportación de datos en `.csv` y `.pdf`.

---

## 4. Usabilidad (Usability)
Grado en que el software puede ser utilizado por usuarios específicos.

*   **Capacidad de Aprendizaje**: Interfaz intuitiva basada en **FullCalendar**, familiar para usuarios acostumbrados a calendarios digitales.
*   **Operatividad**: Menús responsivos y diseño móvil optimizado mediante **Bootstrap 5**, permitiendo el uso en Android, iPhone y Tabletas.
*   **Estética de la Interfaz**: Implementación del branding institucional SENA (Verde `#39A900`) para mejorar la familiaridad del usuario.
*   **Accesibilidad (ARIA)**: Etiquetas ARIA implementadas en `base.html` y plantillas de navegación para compatibilidad con lectores de pantalla.

---

## 5. Fiabilidad (Reliability)
Capacidad de mantener un nivel específico de desempeño bajo condiciones establecidas.

*   **Madurez**: Validaciones de backend (`clean()` en modelos) que previenen estados de datos incoherentes o "choques" de reservas.
*   **Tolerancia a Fallos**: Sistema de logs de errores centralizado y validaciones de formularios que impiden que un error de usuario detenga la ejecución del servidor.
*   **Capacidad de Recuperación**: Arquitectura transaccional de Django/MySQL que asegura la integridad de los datos ante cierres inesperados.

---

## 6. Seguridad (Security)
Protección de la información y los datos.

*   **Confidencialidad**: Implementación de **RBAC (Role-Based Access Control)** con tres perfiles: Admin (Control total), Operativo (Gestión) y Consulta (Solo lectura).
*   **Integridad**: Protección contra ataques CSRF (Cross-Site Request Forgery) mediante el middleware nativo de Django.
*   **Responsabilidad**: Registro de auditoría mediante **Signals** que traquea creación y modificación de registros.
*   **Autenticación**: Sistema de login robusto con persistencia segura y control de fallos.

---

## 7. Mantenibilidad (Maintainability)
Grado de efectividad y eficiencia con que el software puede ser modificado.

*   **Modularidad**: Estructura dividida en aplicaciones Django (`usuarios`, `salas`, `reservas`, `informes`) independientes y reutilizables.
*   **Reusabilidad**: Uso de Mixins y clases base en las vistas para evitar la duplicidad de código.
*   **Capacidad de Prueba**: Suite de pruebas unitarias integradas para validar las reglas de negocio críticas de forma automatizada.

---

## 8. Portabilidad (Portability)
Grado de efectividad y eficiencia con que el software puede ser transferido de un entorno a otro.

*   **Adaptabilidad**: Configuración flexible mediante archivos `.env` para facilitar el cambio entre entornos de desarrollo, pruebas y producción.
*   **Capacidad de Instalación**: Guías detalladas de instalación para Windows y Hosting entregadas al usuario.
*   **Capacidad de Reemplazo**: Preparado para dockerización (`Dockerfile` y `docker-compose.yml`) permitiendo la migración instantánea a entornos en la nube.

---
**Documento Generado el**: 24 de Febrero de 2026
**Responsable de Calidad**: Antigravity AI
