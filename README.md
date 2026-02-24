# Sistema de Agendamiento de Salas de Juntas - SENA 🏢📅

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Django](https://img.shields.io/badge/Django-5.0-green)
![Status](https://img.shields.io/badge/Estado-v1.1.0-success)
![SENA](https://img.shields.io/badge/SENA-Centro_de_la_Construcción-orange)

Sistema web profesional para la gestión, reserva y administración de la Sal de Juntas del **SENA Centro de la Construcción** (Cali). Este sistema optimiza el uso de los espacios físicos mediante un calendario interactivo y reglas de negocio automatizadas.

## 🚀 Características Principales

### 📅 Gestión de Reservas
- **Calendario Interactivo**: Visualización mensual/semanal (FullCalendar) de la disponibilidad.
- **Validación Anti-Conflictos**: Impide automáticamente el solapamiento de reuniones (cruces de horario).
- **Reglas de Calidad**:
  - Horario de operación restringido (7:00 AM - 9:30 PM).
  - Buffer de limpieza de 15 minutos entre reuniones.
  - Validación de capacidad eficiente para evitar sub-utilización.
- **Estados de Reserva**: Confirmada ✅, Pendiente ⏳ y Cancelada ❌ (visible en rojo).

### 👥 Control de Acceso (RBAC)
- **Super Usuario**: Administración total del sistema.
- **Operativo**: Gestión de reservas propias (crear, editar, cancelar).
- **Consulta**: Acceso de solo lectura para visualizar disponibilidad.

### 📱 Diseño Responsivo
- Interfaz adaptada 100% a dispositivos móviles y tablets.
- Menú lateral (Offcanvas) para filtros en móviles.
- **Branding Institucional**: Identidad visual oficial del SENA (Verde Corporativo y Escudo).

### 📊 Reportes e Informes
- Estadísticas de ocupación por sala y usuario.
- Exportación de datos a Excel y PDF.

---

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python, Django 5.0
- **Base de Datos**: MySQL (compatible con SQLite para desarrollo)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Librerías Clave**: `fullcalendar`, `django-crispy-forms`, `reportlab`

---

## 🔧 Instalación y Despliegue

### Requisitos Previos
- Python 3.10 o superior
- Git
- Entorno virtual (recomendado)

### Pasos Rápidos
1.  **Clonar el repositorio**:
    ```bash
    git clone https://github.com/edelgado-1975/Sala_de_juntas.git
    cd Sala_de_juntas
    ```

2.  **Crear entorno virtual**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar migraciones**:
    ```bash
    python manage.py migrate
    ```

5.  **Iniciar servidor**:
    ```bash
    python manage.py runserver
    ```

Visita `http://localhost:8000` en tu navegador.

---

## 📄 Licencia
Este proyecto es de uso exclusivo para el **SENA - Centro de la Construcción**.
**Versión Actual**: v1.1.0
