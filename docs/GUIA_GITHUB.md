# Guía Completa de Git y GitHub

## 🎯 Introducción

Esta guía te ayudará a usar Git y GitHub para mantener el código del Sistema de Agendamiento de Sala de Juntas bajo control de versiones.

## ¿Qué es Git?

Git es un sistema de control de versiones que te permite:
- Guardar el historial de cambios de tu código
- Trabajar en diferentes versiones simultáneamente
- Colaborar con otros desarrolladores
- Recuperar versiones anteriores si algo sale mal

## ¿Qué es GitHub?

GitHub es una plataforma en la nube que:
- Almacena tus repositorios Git
- Permite colaboración en equipo
- Proporciona respaldo automático de tu código
- Facilita el despliegue y la integración continua

## 📥 Instalación de Git en Windows

### Descargar Git

1. Ve a: https://git-scm.com/download/win
2. Descarga la versión más reciente
3. Ejecuta el instalador

### Configuración Inicial

Abre PowerShell o CMD y ejecuta:

```powershell
# Configurar tu nombre
git config --global user.name "Tu Nombre"

# Configurar tu email
git config --global user.email "tu.email@sena.edu.co"

# Verificar configuración
git config --list
```

## 🚀 Flujo de Trabajo Básico

### 1. Ver Estado del Repositorio

```powershell
git status
```

Este comando muestra:
- Archivos modificados
- Archivos nuevos
- Archivos listos para commit

### 2. Agregar Archivos al Staging

```powershell
# Agregar un archivo específico
git add archivo.py

# Agregar todos los archivos modificados
git add .

# Agregar archivos por extensión
git add *.py
```

### 3. Hacer Commit (Guardar Cambios)

```powershell
# Commit con mensaje descriptivo
git commit -m "feat: agregar validación de reservas"

# Commit con mensaje detallado
git commit -m "fix: corregir error en calendario

- Se corrigió el cálculo de fechas
- Se agregó validación de horarios
- Se actualizó la documentación"
```

### 4. Subir Cambios a GitHub

```powershell
# Push a la rama principal
git push origin main

# Push a otra rama
git push origin nombre-rama
```

### 5. Traer Cambios de GitHub

```powershell
# Pull de la rama actual
git pull

# Pull de rama específica
git pull origin main
```

## 🌳 Trabajar con Ramas

### Crear y Cambiar de Rama

```powershell
# Crear nueva rama
git branch feature/nueva-funcionalidad

# Cambiar a una rama
git checkout feature/nueva-funcionalidad

# Crear y cambiar en un solo comando
git checkout -b feature/nueva-funcionalidad
```

### Ver Ramas

```powershell
# Ver ramas locales
git branch

# Ver ramas remotas
git branch -r

# Ver todas las ramas
git branch -a
```

### Fusionar Ramas

```powershell
# Cambiar a la rama destino (ej: main)
git checkout main

# Fusionar otra rama
git merge feature/nueva-funcionalidad
```

## 🐙 Conectar con GitHub

### Crear Repositorio en GitHub

1. Ve a: https://github.com
2. Inicia sesión o crea una cuenta
3. Haz clic en "New Repository"
4. Nombra tu repositorio: `SalaJuntasCC`
5. Elige privado o público
6. NO inicialices con README (ya lo tenemos)
7. Clic en "Create Repository"

### Conectar Repositorio Local

```powershell
# Agregar remote de GitHub
git remote add origin https://github.com/TU-USUARIO/SalaJuntasCC.git

# Verificar remote
git remote -v

# Push inicial
git push -u origin main
```

### Autenticación HTTPS

GitHub requiere autenticación. Opciones:

**Opción 1: Personal Access Token (Recomendado)**

1. En GitHub: Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. Selecciona permisos: `repo` completo
4. Copia el token generado
5. Al hacer push, usa el token como contraseña

**Opción 2: GitHub Desktop**

1. Descarga GitHub Desktop: https://desktop.github.com/
2.Instala y sincroniza con tu cuenta
3. Clona o agrega tu repositorio

## 📝 Convenciones de Commits

Usa mensajes descriptivos con prefijos:

```
feat: nueva funcionalidad
fix: corrección de bugs
docs: cambios en documentación
style: format, cambios de estilo
refactor: refactorización de código
test: agregar o modificar tests
chore: tareas de mantenimiento
```

### Ejemplos Buenos

```powershell
git commit -m "feat: agregar exportación a Google Calendar"
git commit -m "fix: corregir validación de horarios en reservas"
git commit -m "docs: actualizar README con instrucciones de instalación"
```

### Ejemplos Malos

```powershell
git commit -m "cambios"
git commit -m "fix"
git commit -m "actualizacion"
```

## 🏷️ Versionado Semántico

Usa tags para versiones:

```powershell
# Crear tag
git tag -a v1.0.0 -m "Primera versión estable"

# Push de tags
git push origin v1.0.0

# Ver tags
git tag
```

**Formato:** `v<MAJOR>.<MINOR>.<PATCH>`

- **MAJOR:** Cambios incompatibles
- **MINOR:** Nueva funcionalidad compatible
- **PATCH:** Correcciones de bugs

## 🛠️ Comandos Útiles

### Ver Historial

```powershell
# Ver commits
git log

# Ver commits resumido
git log --oneline

# Ver últimos 5 commits
git log -5

# Ver cambios gráficos
git log --graph --oneline --all
```

### Ver Diferencias

```powershell
# Ver cambios no staged
git diff

# Ver cambios staged
git diff --staged

# Ver diferencias entre ramas
git diff main..feature/nueva-funcionalidad
```

### Deshacer Cambios

```powershell
# Descartar cambios en archivo
git checkout -- archivo.py

# Quitar archivo de staging
git reset HEAD archivo.py

# Volver al commit anterior (cuidado!)
git reset --hard HEAD~1
```

### Guardar Temporalmente

```powershell
# Guardar cambios sin commit
git stash

# Ver stashes guardados
git stash list

# Recuperar stash
git stash pop
```

## 🔄 Workflow Recomendado

### Para Feature Nueva

```powershell
# 1. Actualizar main
git checkout main
git pull origin main

# 2. Crear rama feature
git checkout -b feature/calendario-export

# 3. Trabajar y commits
git add .
git commit -m "feat: agregar exportación ICS"

# 4. Push de rama
git push origin feature/calendario-export

# 5. En GitHub: crear Pull Request

# 6. Después de aprobar, fusionar
git checkout main
git pull origin main
git merge feature/calendario-export

# 7. Eliminar rama local
git branch -d feature/calendario-export
```

## 🚫 Archivo .gitignore

Ya está configurado para excluir:

- `.env` (credenciales)
- `__pycache__/` (cache Python)
- `media/` (uploads usuarios)
- `staticfiles/` (archivos estáticos)
- `venv/` (entorno virtual)
- `db.sqlite3` (base de datos local)

**NUNCA** subas a Git:
- Contraseñas o tokens
- Archivos .env
- Datos sensibles

## 💡 Buenas Prácticas

✅ **Hacer commits frecuentes** - Es mejor muchos commits pequeños que uno grande

✅ **Mensajes descriptivos** - Explica QUÉ y POR QUÉ cambiasteCode

✅ **Pull antes de Push** - Siempre trae cambios antes de subir

✅ **Una funcionalidad por rama** - No mezcles features diferentes

✅ **Revisar antes de commit** - Usa `git diff` y `git status`

❌ **No hacer commit de archivos grandes** - Usa .gitignore

❌ **No modificar historial público** - No uses rebase en ramas compartidas

❌ **No commit de código roto** - Asegúrate que funcione

## 📱 GitHub Desktop (Alternativa Visual)

Si prefieres una interfaz gráfica:

1. Descarga: https://desktop.github.com/
2. Instala y conecta tu cuenta GitHub
3. Operaciones disponibles:
   - Ver cambios visual
   - Commits con un clic
   - Push/Pull fácil
   - Gestión de ramas visual

## 🆘 Resolución de Problemas

### Error: "Permission denied"

Configura autenticación con Personal Access Token

### Error: "Merge conflict"

```powershell
# Ver archivos en conflicto
git status

# Editar manualmente los archivos
# Busca marcadores: <<<<<<, =======, >>>>>>>

# Después de resolver
git add archivo-resuelto.py
git commit -m "fix: resolver conflicto de merge"
```

### Error: "Your branch is behind"

```powershell
# Traer cambios remotos
git pull origin main

# Si hay conflictos, resolverlos
```

## 📚 Recursos Adicionales

- **Documentación oficial Git:** https://git-scm.com/doc
- **GitHub Guides:** https://guides.github.com/
- **Git Cheat Sheet:** https://education.github.com/git-cheat-sheet-education.pdf

---

**¡Ahora estás listo para usar Git y GitHub profesionalmente!** 🚀
