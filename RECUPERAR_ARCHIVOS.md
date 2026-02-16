# 🔄 Guía de Recuperación de Archivos

Esta guía te ayudará a recuperar archivos que parecen haberse "perdido" o borrado.

## 🔍 Paso 1: Verificar si el Archivo Existe

### Opción 1: Listar archivos en el directorio

```bash
# Linux/Mac
ls -la *.md

# Windows (CMD)
dir *.md

# Windows (PowerShell)
Get-ChildItem *.md
```

### Opción 2: Buscar el archivo específico

```bash
# Verificar INICIO_RAPIDO.md
ls -la INICIO_RAPIDO.md

# En Windows
dir INICIO_RAPIDO.md
```

### Opción 3: Script de verificación automática

```bash
python verificar_archivos.py
```

---

## 📂 Paso 2: Verificar el Directorio Correcto

A veces el problema es que estás en otro directorio.

```bash
# Ver dónde estás
pwd  # Linux/Mac
cd   # Windows

# Ir al directorio correcto
cd /ruta/al/proyecto/Licitia

# Listar archivos
ls -la
```

**Estructura esperada:**
```
Licitia/
├── INICIO_RAPIDO.md          ← DEBE estar aquí
├── GUIA_INSTALACION.md
├── COMO_REPORTAR_ERRORES.md
├── README.md
├── main.py
└── ... otros archivos
```

---

## 🔄 Paso 3: Recuperar Archivos con Git

Si el archivo realmente se borró, puedes recuperarlo desde Git.

### Método 1: Recuperar desde HEAD (último commit)

```bash
# Recuperar archivo específico
git checkout HEAD -- INICIO_RAPIDO.md

# Verificar que se recuperó
ls -la INICIO_RAPIDO.md
```

### Método 2: Usar git restore (Git 2.23+)

```bash
# Recuperar archivo
git restore INICIO_RAPIDO.md

# O desde staging
git restore --staged INICIO_RAPIDO.md
```

### Método 3: Recuperar desde un commit específico

```bash
# Ver historial del archivo
git log -- INICIO_RAPIDO.md

# Recuperar desde un commit específico
git checkout <commit-hash> -- INICIO_RAPIDO.md
```

### Método 4: Recuperar desde la rama remota

```bash
# Actualizar desde remoto
git fetch origin

# Recuperar archivo desde la rama remota
git checkout origin/main -- INICIO_RAPIDO.md
```

---

## 🔎 Paso 4: Buscar el Archivo en el Sistema

Si no encuentras el archivo en el directorio esperado:

### Linux/Mac

```bash
# Buscar en todo el home
find ~ -name "INICIO_RAPIDO.md"

# Buscar desde el directorio actual
find . -name "INICIO_RAPIDO.md"

# Buscar en todo el sistema (puede tomar tiempo)
sudo find / -name "INICIO_RAPIDO.md" 2>/dev/null
```

### Windows (CMD)

```cmd
dir /s /b INICIO_RAPIDO.md
```

### Windows (PowerShell)

```powershell
Get-ChildItem -Path C:\ -Filter INICIO_RAPIDO.md -Recurse -ErrorAction SilentlyContinue
```

---

## 📊 Paso 5: Ver el Estado de Git

```bash
# Ver estado de archivos
git status

# Ver archivos modificados
git diff --name-only

# Ver archivos borrados
git ls-files --deleted

# Ver historial de cambios
git log --oneline --all -- INICIO_RAPIDO.md
```

---

## 💾 Paso 6: Descargar Archivo Directo desde GitHub

Si todo falla, descarga el archivo directamente:

### Opción 1: Desde GitHub Web

1. Ve a: https://github.com/danielojedameza-png/Licitia
2. Click en `INICIO_RAPIDO.md`
3. Click en "Raw"
4. Guarda el archivo (Ctrl+S o Cmd+S)

### Opción 2: Usando curl

```bash
curl -o INICIO_RAPIDO.md https://raw.githubusercontent.com/danielojedameza-png/Licitia/main/INICIO_RAPIDO.md
```

### Opción 3: Usando wget

```bash
wget https://raw.githubusercontent.com/danielojedameza-png/Licitia/main/INICIO_RAPIDO.md
```

---

## 🚨 Solución de Problemas Comunes

### Problema 1: "Permission denied"

```bash
# Ver permisos
ls -la INICIO_RAPIDO.md

# Cambiar permisos (Linux/Mac)
chmod 644 INICIO_RAPIDO.md

# Cambiar propietario
sudo chown $USER INICIO_RAPIDO.md
```

### Problema 2: "No such file or directory"

**Causas posibles:**
1. Estás en el directorio incorrecto → `cd` al directorio correcto
2. El archivo está en otra rama → `git checkout <rama>`
3. El archivo realmente no existe → Recuperar con `git checkout HEAD --`

### Problema 3: El archivo existe pero no lo ves en tu editor

**Soluciones:**
1. Recargar el editor (F5 o Cmd+R)
2. Cerrar y abrir el proyecto
3. Verificar filtros de archivos en el editor
4. Usar terminal: `cat INICIO_RAPIDO.md`

### Problema 4: "The file is in the index but not in the working tree"

```bash
# El archivo está en staging pero no en disco
git restore --staged INICIO_RAPIDO.md
git restore INICIO_RAPIDO.md
```

---

## 🛠️ Script de Recuperación Automática

Crea un script `recuperar.sh` (Linux/Mac) o `recuperar.bat` (Windows):

### Linux/Mac

```bash
#!/bin/bash
echo "Verificando archivos importantes..."

archivos=("INICIO_RAPIDO.md" "GUIA_INSTALACION.md" "COMO_REPORTAR_ERRORES.md" "README.md")

for archivo in "${archivos[@]}"; do
    if [ ! -f "$archivo" ]; then
        echo "❌ $archivo no encontrado. Recuperando..."
        git checkout HEAD -- "$archivo"
        
        if [ -f "$archivo" ]; then
            echo "✅ $archivo recuperado exitosamente"
        else
            echo "❌ No se pudo recuperar $archivo"
        fi
    else
        echo "✅ $archivo OK"
    fi
done

echo "Verificación completa!"
```

### Windows (recuperar.bat)

```batch
@echo off
echo Verificando archivos importantes...

set archivos=INICIO_RAPIDO.md GUIA_INSTALACION.md COMO_REPORTAR_ERRORES.md README.md

for %%f in (%archivos%) do (
    if not exist %%f (
        echo ❌ %%f no encontrado. Recuperando...
        git checkout HEAD -- %%f
        if exist %%f (
            echo ✅ %%f recuperado exitosamente
        ) else (
            echo ❌ No se pudo recuperar %%f
        )
    ) else (
        echo ✅ %%f OK
    )
)

echo Verificación completa!
pause
```

---

## 📋 Checklist de Recuperación

Sigue estos pasos en orden:

- [ ] 1. Verificar que estás en el directorio correcto (`pwd`)
- [ ] 2. Listar archivos en el directorio (`ls -la *.md`)
- [ ] 3. Ver estado de Git (`git status`)
- [ ] 4. Intentar recuperar con `git checkout HEAD -- INICIO_RAPIDO.md`
- [ ] 5. Si no funciona, buscar el archivo (`find ~ -name "INICIO_RAPIDO.md"`)
- [ ] 6. Si no está, descargar desde GitHub
- [ ] 7. Verificar recuperación (`ls -la INICIO_RAPIDO.md`)
- [ ] 8. Ver contenido (`cat INICIO_RAPIDO.md | head -20`)

---

## 🆘 Si Nada Funciona

### Opción 1: Clonar el repositorio de nuevo

```bash
# Ir al directorio padre
cd ..

# Renombrar directorio actual
mv Licitia Licitia_old

# Clonar de nuevo
git clone https://github.com/danielojedameza-png/Licitia.git
cd Licitia

# Verificar archivo
ls -la INICIO_RAPIDO.md
```

### Opción 2: Contactar Soporte

Si después de seguir todos estos pasos el archivo sigue sin aparecer:

1. Ejecuta: `python collect_diagnostics.py`
2. Genera el archivo ZIP
3. Reporta en: https://github.com/danielojedameza-png/Licitia/issues
4. Incluye:
   - Qué pasos seguiste
   - Output de `git status`
   - Output de `ls -la`
   - El archivo de diagnóstico

---

## 📖 Ver Contenido del Archivo Ahora

Si el archivo existe pero quieres verlo sin abrirlo en editor:

```bash
# Ver todo el archivo
cat INICIO_RAPIDO.md

# Ver primeras 50 líneas
cat INICIO_RAPIDO.md | head -50

# Ver con paginación
less INICIO_RAPIDO.md

# En Windows
type INICIO_RAPIDO.md
more INICIO_RAPIDO.md
```

---

## 🔗 Enlaces Útiles

- **Repositorio**: https://github.com/danielojedameza-png/Licitia
- **Archivo en línea**: https://github.com/danielojedameza-png/Licitia/blob/main/INICIO_RAPIDO.md
- **Issues**: https://github.com/danielojedameza-png/Licitia/issues
- **Git Documentation**: https://git-scm.com/docs

---

**¿Necesitas más ayuda?** Ejecuta:
```bash
python verificar_archivos.py
```

Este script verificará automáticamente todos los archivos importantes y te dirá cuáles faltan.
