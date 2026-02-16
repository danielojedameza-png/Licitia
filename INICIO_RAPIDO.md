# 🚀 Guía Rápida de Inicio - LicitIA

Esta guía te ayudará a comenzar a usar LicitIA en minutos.

## ⚡ Inicio Rápido (3 minutos)

### 1. Clonar el repositorio

```bash
git clone https://github.com/danielojedameza-png/Licitia.git
cd Licitia
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Verificar instalación

```bash
python verify_installation.py
```

Deberías ver: ✅ **INSTALACIÓN VERIFICADA CORRECTAMENTE**

### 5. Iniciar el servidor

```bash
python main.py
```

El servidor estará disponible en: **http://localhost:8000**

### 6. Ver la documentación

Abre en tu navegador:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 7. Probar que funciona

En otra terminal:

```bash
python quick_test.py
```

Deberías ver: ✅ **TODAS LAS PRUEBAS PASARON**

---

## 📚 Documentación Completa

### Para Usuarios
- **[GUIA_INSTALACION.md](GUIA_INSTALACION.md)** - Instalación paso a paso detallada
- **[COMO_REPORTAR_ERRORES.md](COMO_REPORTAR_ERRORES.md)** - Cómo reportar bugs efectivamente
- **[README.md](README.md)** - Documentación técnica completa
- **[USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)** - Ejemplos de uso prácticos

### Para Desarrolladores
- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - Guía técnica de integración
- **[EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)** - Resumen ejecutivo del proyecto

---

## 🛠️ Scripts Útiles

### `verify_installation.py` - Verificar que todo está instalado

```bash
python verify_installation.py
```

Verifica:
- ✅ Versión de Python
- ✅ Dependencias instaladas
- ✅ Estructura del proyecto
- ✅ Módulos importables
- ✅ Tests funcionando
- ✅ Puerto disponible

### `quick_test.py` - Probar todos los endpoints

```bash
# Prueba básica
python quick_test.py

# Guardar reporte
python quick_test.py --save-report

# URL personalizada
python quick_test.py --url http://localhost:8080
```

Prueba:
- Health checks (3 endpoints)
- Planes de suscripción
- Cálculo de precios PLUS
- Cálculo de precios PRO
- Cotización completa
- Modo capeado
- Descuentos por paquete

### `collect_diagnostics.py` - Recopilar información para debugging

```bash
python collect_diagnostics.py
```

Genera un archivo ZIP con:
- Información del sistema
- Paquetes instalados
- Logs recientes
- Estado de archivos del proyecto
- Información de Git

---

## 🎯 Ejemplo Completo

### Calcular Precio PLUS

```bash
curl -X POST http://localhost:8000/api/pricing/plus \
  -H "Content-Type: application/json" \
  -d '{
    "assets": 500000000,
    "process_value": 100000000
  }'
```

Respuesta:
```json
{
  "asset_band": "A2",
  "process_band": "V2",
  "minimum_by_assets": 49900,
  "percentage_price": 60000,
  "base_price": 60000,
  "social_discount": 0,
  "final_price": 60000,
  "explanation": "PLUS price based on process value (0.06% of $100,000,000)"
}
```

### Calcular Precio PRO

```bash
curl -X POST http://localhost:8000/api/pricing/pro \
  -H "Content-Type: application/json" \
  -d '{
    "assets": 500000000,
    "process_value": 300000000,
    "num_annexes": 8
  }'
```

### Análisis Completo (DEMO)

```bash
curl -X POST http://localhost:8000/api/analysis/demo \
  -H "Content-Type: application/json" \
  -d '{
    "certificado": "CERTIFICADO DE EXISTENCIA...",
    "rut": "REGISTRO UNICO TRIBUTARIO...",
    "aviso": "AVISO DE CONVOCATORIA..."
  }'
```

---

## 🐛 ¿Encontraste un Error?

### 1. Recopila el diagnóstico

```bash
python collect_diagnostics.py
```

### 2. Sigue la guía de reporte

Ver: **[COMO_REPORTAR_ERRORES.md](COMO_REPORTAR_ERRORES.md)**

### 3. Reporta en GitHub Issues

https://github.com/danielojedameza-png/Licitia/issues

Incluye:
- Descripción del problema
- Pasos para reproducir
- Mensaje de error completo
- Archivo `diagnostics_*.zip`

---

## 📊 Funcionalidades Principales

### 1. Sistema de Monetización (3 Pilares)

#### Pillar 1: Suscripciones Mensuales
- **POPULAR**: $19,900/mes (30 mensajes)
- **PYME**: $49,900/mes (120 mensajes)
- **EMPRESA**: $129,900/mes (400 mensajes)

#### Pillar 2: Pago por Proceso
- **PLUS**: Validación rápida ($19,900 - $79,900)
- **PRO**: Análisis completo ($49,900 - $1,490,000)

#### Pillar 3: PREMIUM
- Cotización personalizada para casos complejos

### 2. Sistema de Análisis de Licitaciones

- Extracción de datos de PDFs (Certificado, RUT, Aviso)
- Comparación de similitud multi-algoritmo
- Validación estructural y financiera
- Score de 0-100 puntos
- Sistema de semáforo (🟢🟡🔴)
- Recomendaciones inteligentes

### 3. Características Adicionales

- Descuento social (-30%)
- Descuentos por paquete (15-25%)
- Modo dual (Enterprise / Capped 20-80K)
- API REST completa
- Documentación interactiva
- Sistema de logging profesional

---

## 🔧 Solución Rápida de Problemas

### El servidor no arranca

```bash
# Verificar que el puerto no esté en uso
netstat -ano | findstr :8000  # Windows
lsof -ti:8000  # Linux/Mac

# Usar otro puerto
uvicorn main:app --port 8080
```

### Tests fallan

```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall

# Ejecutar con más información
pytest -vv --tb=short
```

### Error: No module named 'X'

```bash
# Asegúrate de tener el entorno virtual activado
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# Reinstalar dependencias
pip install -r requirements.txt
```

---

## 📞 Soporte

### Documentación
- Guías en el repositorio (ver arriba)
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Issues
- GitHub: https://github.com/danielojedameza-png/Licitia/issues

### Scripts de Ayuda
- `python verify_installation.py` - Verificar instalación
- `python quick_test.py` - Probar endpoints
- `python collect_diagnostics.py` - Recopilar información

---

## ✅ Checklist para Empezar

- [ ] Python 3.8+ instalado
- [ ] Repositorio clonado
- [ ] Entorno virtual creado
- [ ] Dependencias instaladas
- [ ] `verify_installation.py` ejecutado con éxito
- [ ] Servidor corriendo
- [ ] `quick_test.py` ejecutado con éxito
- [ ] Documentación revisada en /docs

**¡Listo para usar LicitIA! 🚀**

---

## 🎓 Próximos Pasos

1. **Explora la API**: http://localhost:8000/docs
2. **Lee los ejemplos**: [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)
3. **Integra con tu aplicación**: [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)
4. **Contribuye**: Reporta bugs, sugiere mejoras

---

**Versión**: 2.0.0  
**Última actualización**: Febrero 2024  
**Licencia**: [Ver LICENSE]
