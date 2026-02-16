# 📍 ¿Dónde está la Documentación?

## Ubicación de Todos los Archivos

Todos los archivos de documentación están en el **directorio raíz** del proyecto:

```
Licitia/
├── 🚀 INICIO_RAPIDO.md               ← Guía rápida (3 minutos)
├── 📦 GUIA_INSTALACION.md            ← Instalación paso a paso
├── 🐛 COMO_REPORTAR_ERRORES.md       ← Cómo reportar bugs
├── 💡 USAGE_EXAMPLES.md              ← Ejemplos de uso
├── 📖 README.md                      ← Documentación principal (inglés)
├── 🔧 INTEGRATION_GUIDE.md           ← Guía técnica de integración
├── 📊 EXECUTIVE_SUMMARY.md           ← Resumen ejecutivo
├── ✅ VERIFICATION_REPORT.md         ← Reporte de verificación
├── 🔄 COMPATIBILITY_ANALYSIS.md      ← Análisis de compatibilidad
├── verify_installation.py            ← Script de verificación
├── quick_test.py                     ← Script de pruebas rápidas
├── collect_diagnostics.py            ← Recopilador de diagnósticos
├── main.py                           ← Servidor principal
└── requirements.txt                  ← Dependencias
```

## 📚 Archivos por Propósito

### Para Empezar Rápido
1. **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** - Lee esto primero (3 minutos)
2. **[GUIA_INSTALACION.md](GUIA_INSTALACION.md)** - Instalación detallada
3. `python verify_installation.py` - Verifica que todo funciona

### Para Usar el Sistema
- **[USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)** - Ejemplos en curl, Python, JavaScript
- **[README.md](README.md)** - Documentación completa de la API
- http://localhost:8000/docs - Swagger UI (cuando el servidor esté corriendo)

### Para Reportar Problemas
- **[COMO_REPORTAR_ERRORES.md](COMO_REPORTAR_ERRORES.md)** - Guía de reporte
- `python collect_diagnostics.py` - Recopila información para debugging

### Para Desarrolladores
- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - Guía técnica
- **[EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)** - Arquitectura y métricas

## 🔍 Cómo Abrir los Archivos

### En Windows
```cmd
notepad INICIO_RAPIDO.md
```

### En Linux/Mac
```bash
cat INICIO_RAPIDO.md
# o
less INICIO_RAPIDO.md
# o
nano INICIO_RAPIDO.md
```

### En Visual Studio Code
```bash
code INICIO_RAPIDO.md
```

### En el Navegador (GitHub)
Si estás en GitHub, simplemente haz clic en el archivo en la lista de archivos.

## 🌐 En GitHub Web

Todos los archivos están visibles en:
https://github.com/danielojedameza-png/Licitia

Haz clic en cualquier archivo `.md` para verlo formateado.

## 💡 Consejo Rápido

**Si solo tienes 3 minutos**, lee:
```bash
cat INICIO_RAPIDO.md
```

**Si tienes 10 minutos**, lee también:
```bash
cat GUIA_INSTALACION.md
```

**Si encontraste un error**, ejecuta:
```bash
python collect_diagnostics.py
cat COMO_REPORTAR_ERRORES.md
```

## 🎯 Preguntas Frecuentes

### ¿Dónde está INICIO_RAPIDO.md?
**Respuesta**: En el directorio raíz del proyecto, junto con main.py

### ¿Cómo lo abro?
**Respuesta**: 
- Windows: `notepad INICIO_RAPIDO.md`
- Linux/Mac: `cat INICIO_RAPIDO.md`
- VS Code: `code INICIO_RAPIDO.md`
- GitHub: Click en el archivo

### ¿Está en español?
**Respuesta**: Sí, los siguientes archivos están en español:
- INICIO_RAPIDO.md
- GUIA_INSTALACION.md
- COMO_REPORTAR_ERRORES.md

### ¿Dónde está la documentación técnica?
**Respuesta**: 
- README.md (principal, en inglés)
- INTEGRATION_GUIDE.md (técnico)
- http://localhost:8000/docs (API interactiva)

## 📞 Ayuda Adicional

Si aún no encuentras lo que buscas:

1. **Lista todos los archivos markdown**:
   ```bash
   ls -la *.md
   ```

2. **Busca en todo el proyecto**:
   ```bash
   find . -name "*.md"
   ```

3. **Lee el README principal**:
   ```bash
   cat README.md
   ```

---

**¿Necesitas ayuda?**
- GitHub Issues: https://github.com/danielojedameza-png/Licitia/issues
- Lee: [COMO_REPORTAR_ERRORES.md](COMO_REPORTAR_ERRORES.md)
