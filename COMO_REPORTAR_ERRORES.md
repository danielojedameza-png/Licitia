# 🐛 Cómo Reportar Errores - LicitIA

Esta guía te ayudará a reportar errores de manera efectiva para que puedan ser resueltos rápidamente.

## 🎯 Antes de Reportar

### 1. Verifica que sea un error real

- ¿El comportamiento es diferente de lo esperado?
- ¿Has revisado la documentación?
- ¿Has intentado las soluciones en `GUIA_INSTALACION.md`?

### 2. Intenta reproducir el error

- ¿Puedes hacer que el error ocurra de nuevo?
- ¿Sucede siempre o solo a veces?
- ¿Qué pasos exactos lo causan?

### 3. Ejecuta el diagnóstico automático

```bash
python collect_diagnostics.py
```

Esto creará un archivo `diagnostics_FECHA.zip` con información útil.

---

## 📝 Qué Información Incluir

### ✅ Información Obligatoria

#### 1. Descripción del Problema

**Formato:**
```
### Qué intentaba hacer:
[Describe tu objetivo]

### Qué esperaba que sucediera:
[Describe el resultado esperado]

### Qué sucedió en realidad:
[Describe lo que pasó]
```

**Ejemplo:**
```
### Qué intentaba hacer:
Calcular el precio PLUS para un proceso de $100 millones con activos de $500 millones.

### Qué esperaba que sucediera:
Recibir un precio calculado entre $19,900 y $79,900.

### Qué sucedió en realidad:
Recibí un error 500 con el mensaje "division by zero".
```

#### 2. Pasos para Reproducir

Lista exacta de pasos que causaron el error:

```
1. Inicié el servidor con: python main.py
2. Abrí la documentación en http://localhost:8000/docs
3. Probé el endpoint POST /api/pricing/plus
4. Envié este JSON:
   {
     "assets": 500000000,
     "process_value": 100000000
   }
5. Recibí error 500
```

#### 3. Mensaje de Error Completo

Copia y pega el error COMPLETO, incluyendo el stack trace:

```
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "pricing_calculator.py", line 123, in calculate_plus_price
    result = base_price / percentage
ZeroDivisionError: division by zero
```

#### 4. Tu Entorno

```
- Sistema Operativo: Windows 11 / Linux Ubuntu 22.04 / macOS 13
- Versión de Python: 3.11.5
- Versión de LicitIA: (git branch y commit o versión)
- Navegador (si aplica): Chrome 120
```

Para obtener esta información automáticamente:
```bash
python collect_diagnostics.py
```

---

## 🔍 Información Adicional Útil

### Para Errores de API

- **Request completo** (curl, código Python, o captura de Swagger UI)
- **Response completo** (incluyendo código de estado)
- **Headers de request y response**

Ejemplo con curl:
```bash
curl -X POST http://localhost:8000/api/pricing/plus \
  -H "Content-Type: application/json" \
  -d '{"assets": 500000000, "process_value": 100000000}' \
  -v
```

### Para Errores con Archivos PDF

- **Tamaño del archivo** (en MB)
- **Tipo de PDF** (escaneado, digital, con imágenes)
- **Versión de PDF** (si es posible)
- **Ejemplo del archivo** (si no contiene información sensible)

### Para Errores de Instalación

- **Output completo** del comando que falló
- **Contenido de `requirements.txt`**
- **Resultado de**: `pip list`

---

## 📸 Capturas de Pantalla

Las imágenes ayudan mucho:

### Cuándo incluir capturas:

- ✅ Errores visuales en la interfaz
- ✅ Mensajes de error en la consola
- ✅ Comportamiento inesperado en la UI
- ✅ Problemas de instalación

### Cómo hacer buenas capturas:

1. **Captura completa** - Incluye toda la ventana/terminal
2. **Legible** - Asegúrate de que el texto sea legible
3. **Relevante** - Muestra solo lo necesario
4. **Anotada** - Marca con flechas o círculos lo importante

---

## 📋 Logs del Sistema

### Logs de la Aplicación

Los logs se guardan en:
- **Consola**: Lo que ves en terminal
- **Archivo**: `logs/licitia.log`

#### Cómo obtener los logs:

**Últimas 100 líneas:**
```bash
# Windows (PowerShell)
Get-Content logs\licitia.log -Tail 100

# Linux/Mac
tail -n 100 logs/licitia.log
```

**Logs de una sesión específica:**
```bash
# Buscar por fecha/hora
grep "2024-02-16 10:30" logs/licitia.log
```

#### Qué incluir:

- ❌ No incluyas TODO el archivo de log (muy grande)
- ✅ Incluye las líneas relevantes al error
- ✅ Incluye ~20 líneas antes y después del error
- ✅ Incluye el timestamp del error

---

## 🎯 Formato del Reporte

### Template Completo

Copia y pega este template, llenando cada sección:

```markdown
## Descripción del Error

### Qué intentaba hacer:
[Tu descripción aquí]

### Qué esperaba:
[Resultado esperado]

### Qué sucedió:
[Lo que realmente pasó]

## Pasos para Reproducir

1. [Paso 1]
2. [Paso 2]
3. [Paso 3]

## Mensaje de Error

```
[Pega aquí el error completo con stack trace]
```

## Entorno

- **SO**: [Windows/Linux/Mac + versión]
- **Python**: [Versión]
- **LicitIA**: [Branch/commit/versión]
- **Navegador**: [Si aplica]

## Información Adicional

[Cualquier otro detalle relevante]

## Archivos Adjuntos

- [ ] diagnostics.zip (generado con collect_diagnostics.py)
- [ ] Capturas de pantalla (si aplican)
- [ ] Archivo de ejemplo (si aplica y no es sensible)
```

---

## 📧 Dónde Reportar

### Opción 1: GitHub Issues (Recomendado)

1. Ve a: https://github.com/danielojedameza-png/Licitia/issues
2. Click en "New Issue"
3. Usa el template de arriba
4. Adjunta `diagnostics.zip`
5. Envía el issue

### Opción 2: Por Email

Si el error contiene información sensible:

1. Genera el archivo de diagnóstico
2. Envía email a: [EMAIL DE SOPORTE]
3. Asunto: `[BUG] Descripción breve del error`
4. Incluye toda la información del template
5. Adjunta el archivo diagnostics.zip

---

## ⚠️ Información Sensible

### NO incluyas:

- ❌ Contraseñas o tokens
- ❌ Claves API
- ❌ Datos personales de clientes
- ❌ Información financiera real
- ❌ Documentos confidenciales

### Si necesitas incluir un archivo con datos sensibles:

1. Crea una versión de prueba con datos ficticios
2. O reemplaza los datos reales con:
   - `NOMBRE_EMPRESA` → "Empresa de Prueba"
   - `NIT_REAL` → "123456789"
   - Etc.

---

## 🚀 Prioridad de Errores

Para ayudarnos a priorizar, indica la gravedad:

### 🔴 CRÍTICO
- El sistema no arranca
- Pérdida de datos
- Vulnerabilidad de seguridad
- El sistema crashea constantemente

### 🟡 ALTO
- Feature principal no funciona
- Error afecta a muchos usuarios
- Workaround difícil

### 🟢 MEDIO
- Feature secundario no funciona
- Hay workaround disponible
- Afecta experiencia pero no bloquea

### ⚪ BAJO
- Mejora cosmética
- Typo en documentación
- Sugerencia de mejora

**Ejemplo:**
```
## Prioridad: 🔴 CRÍTICO

El servidor no arranca después de instalar las dependencias.
```

---

## ✅ Checklist de Reporte Completo

Antes de enviar tu reporte, verifica:

- [ ] He intentado reproducir el error
- [ ] He incluido pasos claros para reproducir
- [ ] He incluido el mensaje de error completo
- [ ] He incluido información de mi entorno
- [ ] He generado y adjuntado `diagnostics.zip`
- [ ] He incluido capturas de pantalla (si aplica)
- [ ] He eliminado información sensible
- [ ] He indicado la prioridad/gravedad
- [ ] He usado un título descriptivo

---

## 🎓 Ejemplo de Buen Reporte

```markdown
## [BUG] Error de división por cero al calcular precio PLUS con activos en 0

### Descripción

Al intentar calcular el precio PLUS con activos en 0, el sistema devuelve un error 500.

### Pasos para Reproducir

1. Iniciar servidor: `python main.py`
2. Ir a http://localhost:8000/docs
3. Probar endpoint POST /api/pricing/plus
4. Enviar:
   ```json
   {
     "assets": 0,
     "process_value": 100000000
   }
   ```
5. Ver error 500

### Error

```
Traceback (most recent call last):
  File "pricing_calculator.py", line 145, in calculate_plus_price
    percentage_price = process_value * (band_percentage / 100)
ZeroDivisionError: division by zero
```

### Entorno

- SO: Windows 11 Pro
- Python: 3.11.5
- LicitIA: branch main, commit abc123
- Navegador: Chrome 120

### Solución Propuesta

Agregar validación para `assets == 0` o usar el mínimo por defecto (A0).

### Adjuntos

- diagnostics_20240216_103045.zip
- screenshot_error.png
```

---

## 🤝 Después de Reportar

### Qué esperar:

1. **Confirmación**: Recibirás confirmación de que tu reporte fue recibido
2. **Preguntas**: Podemos pedirte información adicional
3. **Actualización**: Te notificaremos cuando se resuelva
4. **Agradecimiento**: ¡Gracias por ayudar a mejorar LicitIA!

### Puedes ayudar más:

- Responde a preguntas adicionales rápidamente
- Prueba el fix cuando esté disponible
- Confirma si el problema se resolvió

---

## 🎉 Gracias por Reportar

Los reportes de errores bien documentados son invaluables para mejorar el sistema. 

**Tu reporte ayuda a todos los usuarios de LicitIA** 🚀

---

## 📚 Referencias

- **Documentación**: `README.md`
- **Guía de instalación**: `GUIA_INSTALACION.md`
- **Guía técnica**: `INTEGRATION_GUIDE.md`
- **Recopilar diagnóstico**: `python collect_diagnostics.py`
- **Verificar instalación**: `python verify_installation.py`
