# 📋 Recomendaciones de Calidad (Basado en ISO/IEC 25000)
## Sistema de Agendamiento de Salas de Juntas - SENA
**Evaluación de Calidad de Producto de Software (SQuaRE)**

La norma **ISO/IEC 25000** define un marco para evaluar la calidad del software. Basado en el estado actual del proyecto (v1.0.0), aquí se presentan recomendaciones clave para elevar el estándar del producto:

---

## 1. Adecuación Funcional
*   **Estado Actual**: El sistema cubre los procesos de agendamiento, visualización y reportes.
*   **Recomendación**: Implementar una **Auditoría de Acciones**. Aunque existe el log técnico, sería ideal que el administrador pueda ver desde la interfaz un historial de quién modificó qué reserva (completitud funcional).

## 2. Eficiencia de Desempeño
*   **Estado Actual**: Excelente para carga moderada.
*   **Recomendación**: Implementar **Caché a nivel de Base de Datos** para el calendario. Al crecer el número de reservas, las consultas al calendario pueden volverse lentas. El uso de `select_related` y `prefetch_related` en los QuerySets de Django es crítico aquí.

## 3. Compatibilidad
*   **Estado Actual**: Alta compatibilidad gracias a Bootstrap 5.
*   **Recomendación**: Realizar pruebas específicas en **navegadores menos comunes** (Safari en iOS antiguo o versiones específicas de Edge en servidores Windows) para asegurar que el calendario (FullCalendar) renderice correctamente.

## 4. Usabilidad
*   **Estado Actual**: Interfaz limpia y con branding SENA.
*   **Recomendación**: Mejorar la **Accesibilidad (A11y)**. Asegurar que todos los elementos tengan etiquetas `aria-label` para lectores de pantalla, cumpliendo con estándares gubernamentales de inclusión.

## 5. Fiabilidad (Reliability)
*   **Estado Actual**: Se han implementado 7 pruebas de negocio.
*   **Recomendación**: Implementar un **Manejo de Fallos en Servidor de Correo**. Si el SMTP de Gmail falla, el sistema no debe "romperse" delante del usuario. Se recomienda usar tareas en segundo plano (como *Celery* o *Django Q*) para que el envío de correos no bloquee la navegación.

## 6. Seguridad
*   **Estado Actual**: RBAC y Time-out de sesión implementados.
*   **Recomendación**: Implementar **Logs de Intentos Fallidos**. Registrar quién intenta entrar y falla, para detectar posibles ataques de fuerza bruta temprano.

## 7. Mantenibilidad
*   **Estado Actual**: Estructura modular por aplicaciones.
*   **Recomendación**: Aumentar la **Cobertura de Código** de las pruebas unitarias. Actualmente cubrimos las reglas de negocio, pero se debería cubrir el 80% de las funciones del sistema para facilitar cambios futuros sin romper nada.

## 8. Portabilidad
*   **Estado Actual**: Manuales para Windows y Hosting entregados.
*   **Recomendación**: Crear una **Imagen de Docker**. Esto permitiría que el sistema se instale en cualquier servidor (Linux, Windows, Cloud) en segundos, eliminando el problema de "en mi máquina funciona".

---

### Resumen de Prioridades (Roadmap de Calidad)

| Prioridad | Característica | Acción Sugerida |
|---|---|---|
| **Alta** | Fiabilidad | Tareas asíncronas para el correo (Evitar bloqueos). |
| **Media** | Mantenibilidad | Incrementar cobertura de tests unitarios. |
| **Media** | Usabilidad | Etiquetas de accesibilidad (Inclusión). |
| **Baja** | Portabilidad | Dockerización del proyecto. |

---
**Nota**: Estas recomendaciones no invalidan la versión actual, sino que marcan la ruta para que el software pase de ser un "Producto Funcional" a un "Producto de Software de Clase Mundial".
