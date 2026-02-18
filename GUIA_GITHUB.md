# Guía de Conexión a GitHub (v1.0.0)

Esta guía explica cómo conectar tu proyecto "Sala de Juntas SENA" con un repositorio remoto en GitHub.

## 1. Obtener la URL del Repositorio
Al crear un nuevo repositorio vacío en GitHub, verás una pantalla con instrucciones.

**Si el repositorio está vacío:**
La URL aparece en la sección "Quick setup", dentro del recuadro gris.
Ejemplo: `https://github.com/TU_USUARIO/NOMBRE_DEL_REPO.git`

**Si el repositorio ya tiene archivos:**
1.  Haz clic en el botón verde **Code** (Código) ubicado arriba a la derecha de la lista de archivos.
2.  Asegúrate de estar en la pestaña **HTTPS**.
3.  Haz clic en el icono de copiar al lado de la URL.

---

## 2. Comandos de Conexión
Abre tu terminal en la carpeta del proyecto (`D:\SalaJuntasCC`) y ejecuta:

### Paso 1: Enlazar el Remoto
```bash
git remote add origin PEGA_AQUI_TU_URL
# Ejemplo: git remote add origin https://github.com/edgar/sala-juntas.git
```

> **Nota**: Si te sale el error `error: remote origin already exists`, significa que ya hay una conexión vieja. Elimínala primero con `git remote remove origin` y repite el paso 1.

### Paso 2: Renombrar Rama Principal
GitHub usa `main` como estándar moderno.
```bash
git branch -M main
```

### Paso 3: Subir el Código
```bash
git push -u origin main
```
Te pedirá tu usuario y contraseña (o Token de Acceso Personal) de GitHub si es la primera vez.

---

## 3. Gestión de Versiones Futuras
Para guardar nuevos cambios en el futuro:

1.  **Guardar localmente**:
    ```bash
    git add .
    git commit -m "Descripción del cambio"
    ```
2.  **Subir a la nube**:
    ```bash
    git push
    ```
