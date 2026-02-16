#!/usr/bin/env python3
"""
Script de recopilación de diagnósticos para LicitIA

Recopila información del sistema, logs y configuración para ayudar en el debugging.
Genera un archivo ZIP con toda la información.
"""

import sys
import os
import platform
import subprocess
import json
import zipfile
from datetime import datetime
from pathlib import Path
import shutil

def get_timestamp():
    """Obtiene timestamp para nombres de archivo"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def get_system_info():
    """Recopila información del sistema"""
    info = {
        "timestamp": datetime.now().isoformat(),
        "system": {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "python_version": sys.version,
            "python_implementation": platform.python_implementation(),
        },
        "python": {
            "version": platform.python_version(),
            "compiler": platform.python_compiler(),
            "build": platform.python_build(),
            "executable": sys.executable,
            "prefix": sys.prefix,
        },
        "paths": {
            "cwd": os.getcwd(),
            "home": str(Path.home()),
        }
    }
    return info

def get_installed_packages():
    """Obtiene lista de paquetes instalados"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--format=json"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return {"error": "Could not get package list", "stderr": result.stderr}
    except Exception as e:
        return {"error": str(e)}

def get_environment_variables():
    """Obtiene variables de entorno relevantes (sin datos sensibles)"""
    relevant_vars = [
        "PATH", "PYTHONPATH", "VIRTUAL_ENV", "PORT", 
        "LOG_LEVEL", "DEBUG_MODE", "ALLOW_CORS"
    ]
    
    env_vars = {}
    for var in relevant_vars:
        value = os.environ.get(var)
        if value:
            # Truncar PATH si es muy largo
            if var == "PATH" and len(value) > 500:
                env_vars[var] = value[:500] + "... [truncated]"
            else:
                env_vars[var] = value
    
    return env_vars

def get_git_info():
    """Obtiene información de Git"""
    try:
        # Branch actual
        branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5
        ).stdout.strip()
        
        # Último commit
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5
        ).stdout.strip()
        
        # Commit corto
        commit_short = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5
        ).stdout.strip()
        
        # Cambios pendientes
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=5
        ).stdout.strip()
        
        return {
            "branch": branch,
            "commit": commit,
            "commit_short": commit_short,
            "has_changes": bool(status),
            "changes_summary": status[:500] if status else "No changes"
        }
    except Exception as e:
        return {"error": str(e), "git_available": False}

def check_project_files():
    """Verifica existencia de archivos clave del proyecto"""
    files_to_check = [
        "main.py",
        "requirements.txt",
        "pricing_calculator.py",
        "pricing_config.py",
        "models.py",
        "demo_engine.py",
        "README.md",
        "core/extractor.py",
        "core/comparador.py",
        "core/validador.py",
        "utils/pdf_handler.py",
    ]
    
    file_status = {}
    for file_path in files_to_check:
        path = Path(file_path)
        if path.exists():
            file_status[file_path] = {
                "exists": True,
                "size": path.stat().st_size,
                "modified": datetime.fromtimestamp(path.stat().st_mtime).isoformat()
            }
        else:
            file_status[file_path] = {"exists": False}
    
    return file_status

def get_recent_logs():
    """Obtiene logs recientes (últimas 500 líneas)"""
    log_file = Path("logs/licitia.log")
    
    if not log_file.exists():
        return "No log file found"
    
    try:
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            # Últimas 500 líneas
            recent_lines = lines[-500:] if len(lines) > 500 else lines
            return ''.join(recent_lines)
    except Exception as e:
        return f"Error reading log file: {str(e)}"

def create_diagnostics_report():
    """Crea el reporte de diagnósticos completo"""
    print("🔍 Recopilando información de diagnóstico...")
    
    report = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "tool_version": "1.0.0",
            "purpose": "LicitIA diagnostics report"
        },
        "system": get_system_info(),
        "packages": get_installed_packages(),
        "environment": get_environment_variables(),
        "git": get_git_info(),
        "project_files": check_project_files(),
    }
    
    return report

def create_diagnostics_zip():
    """Crea archivo ZIP con toda la información de diagnóstico"""
    timestamp = get_timestamp()
    temp_dir = Path(f"diagnostics_{timestamp}")
    zip_filename = f"diagnostics_{timestamp}.zip"
    
    try:
        # Crear directorio temporal
        temp_dir.mkdir(exist_ok=True)
        print(f"📁 Creando directorio temporal: {temp_dir}")
        
        # 1. Reporte JSON
        print("📝 Generando reporte del sistema...")
        report = create_diagnostics_report()
        report_file = temp_dir / "system_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # 2. Requirements.txt
        print("📦 Copiando requirements.txt...")
        if Path("requirements.txt").exists():
            shutil.copy("requirements.txt", temp_dir / "requirements.txt")
        
        # 3. Logs recientes
        print("📜 Recopilando logs...")
        logs = get_recent_logs()
        with open(temp_dir / "recent_logs.txt", 'w', encoding='utf-8') as f:
            f.write(logs)
        
        # 4. Config files (si existen)
        config_files = [".env", "config.ini", "config.json"]
        for config_file in config_files:
            if Path(config_file).exists():
                print(f"⚙️  Copiando {config_file}...")
                # Nota: Ten cuidado con datos sensibles
                shutil.copy(config_file, temp_dir / config_file)
        
        # 5. Readme con instrucciones
        print("📄 Creando README...")
        readme_content = f"""
# Diagnóstico de LicitIA
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Contenido

- **system_report.json**: Información completa del sistema, Python, paquetes instalados
- **requirements.txt**: Dependencias del proyecto
- **recent_logs.txt**: Últimas 500 líneas del log
- **README.txt**: Este archivo

## Uso

Este archivo contiene información de diagnóstico para ayudar a resolver problemas.

Adjunta este archivo ZIP cuando reportes un error.

## Privacidad

IMPORTANTE: Revisa el contenido antes de compartir.
Este archivo NO debe contener:
- Contraseñas o tokens
- Claves API
- Datos personales de clientes
- Información financiera sensible

Si encuentras información sensible, elimínala antes de compartir.

## Información del Sistema

- Sistema Operativo: {platform.system()} {platform.release()}
- Python: {platform.python_version()}
- Directorio: {os.getcwd()}

## Próximos Pasos

1. Revisa el contenido del ZIP
2. Elimina cualquier información sensible si existe
3. Adjunta este archivo a tu reporte de error
4. Incluye descripción del problema y pasos para reproducir

Para más información sobre cómo reportar errores:
Ver: COMO_REPORTAR_ERRORES.md
"""
        with open(temp_dir / "README.txt", 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        # 6. Crear ZIP
        print(f"🗜️  Creando archivo ZIP: {zip_filename}")
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in temp_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(temp_dir)
                    zipf.write(file_path, arcname)
        
        # 7. Limpiar directorio temporal
        print("🧹 Limpiando archivos temporales...")
        shutil.rmtree(temp_dir)
        
        # 8. Éxito
        file_size = Path(zip_filename).stat().st_size / 1024  # KB
        print(f"\n✅ Diagnóstico completado exitosamente!")
        print(f"📦 Archivo creado: {zip_filename} ({file_size:.1f} KB)")
        print(f"\n📋 Próximos pasos:")
        print(f"   1. Revisa el contenido del ZIP (descomprímelo y verifica)")
        print(f"   2. Elimina información sensible si existe")
        print(f"   3. Adjunta este archivo a tu reporte de error")
        print(f"\n📖 Para más información: COMO_REPORTAR_ERRORES.md")
        
        return zip_filename
        
    except Exception as e:
        print(f"\n❌ Error al crear diagnóstico: {str(e)}")
        # Limpiar si hay error
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        raise

def main():
    """Función principal"""
    print("="*60)
    print("🔧 LicitIA - Recopilador de Diagnósticos")
    print("="*60)
    print("\nEste script recopilará información para ayudar a diagnosticar problemas.")
    print("La información incluye:")
    print("  - Información del sistema operativo")
    print("  - Versión de Python y paquetes instalados")
    print("  - Logs recientes de la aplicación")
    print("  - Estado de archivos del proyecto")
    print("\n⚠️  IMPORTANTE: Revisa el archivo generado antes de compartirlo.")
    print("   NO debe contener contraseñas, tokens o datos sensibles.\n")
    
    try:
        response = input("¿Continuar? (s/n): ").lower()
        if response not in ['s', 'si', 'y', 'yes', '']:
            print("Operación cancelada.")
            return 0
        
        print()
        zip_file = create_diagnostics_zip()
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Operación cancelada por el usuario")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
