# 🚀 Guía de Instalación Local - LicitIA

Esta guía te ayudará a instalar y ejecutar LicitIA en tu computadora local para pruebas y desarrollo.

## 📋 Prerrequisitos

Antes de comenzar, asegúrate de tener instalado:

### Obligatorio
- **Python 3.8 o superior** (Recomendado: Python 3.11)
  - Windows: Descarga desde [python.org](https://www.python.org/downloads/)
  - Linux: `sudo apt install python3.11 python3.11-venv`
  - Mac: `brew install python@3.11`

### Verificar instalación de Python
```bash
python --version
# o en algunos sistemas:
python3 --version
```

Deberías ver algo como: `Python 3.11.x` o superior.

---

## 🪟 Instalación en Windows

### Paso 1: Descargar el repositorio

#### Opción A: Con Git (Recomendado)
```bash
# Instalar Git si no lo tienes: https://git-scm.com/download/win
git clone https://github.com/danielojedameza-png/Licitia.git
cd Licitia
```

#### Opción B: Descarga directa
1. Ve a https://github.com/danielojedameza-png/Licitia
2. Click en "Code" → "Download ZIP"
3. Extrae el ZIP en tu carpeta de proyectos
4. Abre PowerShell o CMD en esa carpeta

### Paso 2: Crear entorno virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate

# Verás (venv) al inicio de tu línea de comandos
```

### Paso 3: Instalar dependencias

```bash
# Actualizar pip (recomendado)
python -m pip install --upgrade pip

# Instalar todas las dependencias
pip install -r requirements.txt
```

### Paso 4: Verificar instalación

```bash
python verify_installation.py
```

Si todo está bien, verás: ✅ **Instalación verificada correctamente**

### Paso 5: Ejecutar el servidor

```bash
python main.py
```

O con recarga automática (desarrollo):
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Paso 6: Probar la API

Abre tu navegador en:
- **Documentación interactiva**: http://localhost:8000/docs
- **Documentación alternativa**: http://localhost:8000/redoc
- **Health check**: http://localhost:8000/

---

## 🐧 Instalación en Linux/Mac

### Paso 1: Descargar el repositorio

```bash
git clone https://github.com/danielojedameza-png/Licitia.git
cd Licitia
```

### Paso 2: Crear entorno virtual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Verás (venv) al inicio de tu línea de comandos
```

### Paso 3: Instalar dependencias

```bash
# Actualizar pip (recomendado)
pip install --upgrade pip

# Instalar todas las dependencias
pip install -r requirements.txt
```

### Paso 4: Verificar instalación

```bash
python verify_installation.py
```

### Paso 5: Ejecutar el servidor

```bash
python main.py
```

O con Uvicorn directamente:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🧪 Ejecutar Pruebas

### Ejecutar todos los tests

```bash
# Con pytest (recomendado)
pytest -v

# O con Python directamente
python -m pytest -v
```

### Ejecutar tests específicos

```bash
# Solo tests de pricing
pytest test_pricing_calculator.py -v

# Solo tests de API
pytest test_api.py -v

# Solo tests de análisis
pytest tests/analysis/test_extractor.py -v
```

### Ejecutar prueba rápida del sistema

```bash
python quick_test.py
```

Esto ejecutará pruebas de los endpoints principales y generará un reporte.

---

## 🐛 Verificar que todo funciona

### Test manual con curl

```bash
# 1. Verificar que el servidor responde
curl http://localhost:8000/

# 2. Obtener planes de suscripción
curl http://localhost:8000/api/pricing/subscriptions

# 3. Calcular precio PLUS
curl -X POST http://localhost:8000/api/pricing/plus \
  -H "Content-Type: application/json" \
  -d '{"assets": 500000000, "process_value": 100000000}'
```

### Test manual desde Python

```python
import requests

# Verificar conexión
response = requests.get('http://localhost:8000/')
print(response.json())

# Probar cálculo de precio
data = {
    "assets": 500000000,
    "process_value": 100000000
}
response = requests.post('http://localhost:8000/api/pricing/plus', json=data)
print(response.json())
```

---

## 📊 Visualizar Logs

Los logs se guardan automáticamente en:
- **Consola**: Salida estándar (lo que ves en terminal)
- **Archivo**: `logs/licitia.log` (si está configurado)

Para ver logs en tiempo real:

### Windows (PowerShell)
```powershell
Get-Content logs\licitia.log -Wait -Tail 50
```

### Linux/Mac
```bash
tail -f logs/licitia.log
```

---

## ⚙️ Configuración Avanzada

### Variables de Entorno (Opcional)

Crea un archivo `.env` en la raíz del proyecto:

```env
# Puerto del servidor
PORT=8000

# Nivel de logging (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# Modo de desarrollo
DEBUG_MODE=true

# Permitir CORS desde todos los orígenes
ALLOW_CORS=true
```

### Configurar puerto diferente

```bash
# Opción 1: Variable de entorno
export PORT=8080
python main.py

# Opción 2: Con uvicorn
uvicorn main:app --port 8080
```

---

## 🔧 Solución de Problemas Comunes

### Error: "pip no se reconoce como comando"

**Solución**: Asegúrate de que Python esté en el PATH o usa:
```bash
python -m pip install -r requirements.txt
```

### Error: "No module named 'fastapi'"

**Solución**: Activa el entorno virtual y reinstala:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### Error: "Port 8000 is already in use"

**Solución**: Usa otro puerto:
```bash
uvicorn main:app --port 8080
```

O encuentra y cierra el proceso que usa el puerto:

**Windows:**
```bash
netstat -ano | findstr :8000
taskkill /PID <numero_proceso> /F
```

**Linux/Mac:**
```bash
lsof -ti:8000 | xargs kill -9
```

### Error al instalar PyPDF2

**Solución**: Instala las herramientas de compilación:

**Windows**: Instala [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

**Linux**: 
```bash
sudo apt install build-essential python3-dev
```

**Mac**:
```bash
xcode-select --install
```

### Tests fallan

**Solución**: Verifica que:
1. El entorno virtual está activado
2. Todas las dependencias están instaladas
3. No hay otro servidor corriendo en el puerto 8000

```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall

# Ejecutar tests con más información
pytest -vv --tb=short
```

### Error: "Permission denied" al crear logs

**Solución**: Crea la carpeta de logs manualmente:
```bash
mkdir logs
```

---

## 📱 Probar con archivos PDF

### Preparar archivos de prueba

Coloca tus PDFs de prueba en una carpeta, por ejemplo:
```
test_files/
  ├── certificado_camara.pdf
  ├── rut.pdf
  └── aviso_convocatoria.pdf
```

### Enviar archivos a la API

```python
import requests

files = {
    'certificado': open('test_files/certificado_camara.pdf', 'rb'),
    'rut': open('test_files/rut.pdf', 'rb'),
    'aviso': open('test_files/aviso_convocatoria.pdf', 'rb')
}

response = requests.post(
    'http://localhost:8000/api/analysis/demo-files',
    files=files
)

print(response.json())
```

---

## 🆘 ¿Necesitas Ayuda?

Si tienes problemas:

1. **Ejecuta el diagnóstico automático**:
   ```bash
   python collect_diagnostics.py
   ```
   Esto creará un archivo `diagnostics_FECHA.zip` con toda la información.

2. **Revisa la documentación**:
   - `README.md` - Documentación general
   - `INTEGRATION_GUIDE.md` - Guía técnica detallada
   - `COMO_REPORTAR_ERRORES.md` - Cómo reportar bugs

3. **Reporta el error**:
   - Incluye el archivo de diagnóstico
   - Describe qué intentabas hacer
   - Incluye el mensaje de error completo
   - Indica tu sistema operativo y versión de Python

---

## 🎯 Siguiente Paso

Una vez que tengas el sistema corriendo, consulta:
- **USAGE_EXAMPLES.md** - Ejemplos de uso de la API
- **INTEGRATION_GUIDE.md** - Guía de integración completa
- **Documentación interactiva** - http://localhost:8000/docs

---

## ✅ Checklist de Instalación Exitosa

- [ ] Python 3.8+ instalado
- [ ] Repositorio descargado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas
- [ ] `verify_installation.py` ejecutado exitosamente
- [ ] Servidor corriendo en http://localhost:8000
- [ ] Tests básicos pasan
- [ ] Documentación accesible en /docs

**¡Listo para desarrollar! 🚀**
