#!/usr/bin/env python3
"""
Script de Verificación de Archivos - LicitIA
Verifica que todos los archivos importantes del proyecto estén presentes
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Colores para la terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_colored(text, color):
    """Imprime texto con color"""
    print(f"{color}{text}{Colors.END}")

def print_header(text):
    """Imprime un encabezado"""
    print()
    print("=" * 60)
    print_colored(f"  {text}", Colors.BOLD + Colors.CYAN)
    print("=" * 60)

def check_file(filepath, description=""):
    """Verifica si un archivo existe y muestra información"""
    exists = os.path.exists(filepath)
    filename = os.path.basename(filepath)
    
    if exists:
        size = os.path.getsize(filepath)
        mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
        
        print_colored(f"✓ {filename}", Colors.GREEN)
        print(f"  Ubicación: {os.path.abspath(filepath)}")
        print(f"  Tamaño: {size:,} bytes")
        print(f"  Última modificación: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if description:
            print(f"  Descripción: {description}")
        
        return True
    else:
        print_colored(f"✗ {filename}", Colors.RED)
        print(f"  ❌ ARCHIVO NO ENCONTRADO")
        print(f"  Ubicación esperada: {os.path.abspath(filepath)}")
        
        if description:
            print(f"  Descripción: {description}")
        
        return False

def suggest_recovery(missing_files):
    """Sugiere comandos para recuperar archivos faltantes"""
    if not missing_files:
        return
    
    print_header("Comandos de Recuperación")
    
    print_colored("\n📋 Archivos faltantes detectados:", Colors.YELLOW)
    for f in missing_files:
        print(f"  - {f}")
    
    print_colored("\n🔄 Para recuperar estos archivos, ejecuta:", Colors.CYAN)
    print("\n# Recuperar todos los archivos desde Git:")
    for f in missing_files:
        print(f"git checkout HEAD -- {f}")
    
    print("\n# O recuperar todos a la vez:")
    print("git checkout HEAD -- " + " ".join(missing_files))
    
    print("\n# O descargar desde GitHub:")
    for f in missing_files:
        print(f"curl -o {f} https://raw.githubusercontent.com/danielojedameza-png/Licitia/main/{f}")

def main():
    """Función principal"""
    print_header("🔍 Verificador de Archivos - LicitIA")
    
    print_colored("\nVerificando archivos importantes del proyecto...\n", Colors.CYAN)
    
    # Archivos de documentación
    docs = {
        "INICIO_RAPIDO.md": "Guía rápida de inicio (3 minutos)",
        "GUIA_INSTALACION.md": "Instalación paso a paso detallada",
        "COMO_REPORTAR_ERRORES.md": "Cómo reportar bugs efectivamente",
        "README.md": "Documentación principal del proyecto",
        "INTEGRATION_GUIDE.md": "Guía técnica de integración",
        "EXECUTIVE_SUMMARY.md": "Resumen ejecutivo del proyecto",
        "USAGE_EXAMPLES.md": "Ejemplos de uso prácticos",
        "DONDE_ESTA_LA_DOCUMENTACION.md": "Guía de ubicación de documentos",
        "RECUPERAR_ARCHIVOS.md": "Guía de recuperación de archivos"
    }
    
    # Scripts principales
    scripts = {
        "main.py": "Servidor principal FastAPI",
        "pricing_calculator.py": "Calculadora de precios",
        "pricing_config.py": "Configuración de pricing",
        "models.py": "Modelos Pydantic",
        "demo_engine.py": "Motor de análisis",
        "verify_installation.py": "Script de verificación de instalación",
        "quick_test.py": "Script de pruebas rápidas",
        "collect_diagnostics.py": "Recopilador de diagnósticos",
        "logging_config.py": "Configuración de logging"
    }
    
    # Archivos de configuración
    config = {
        "requirements.txt": "Dependencias Python",
        ".gitignore": "Archivos ignorados por Git"
    }
    
    # Módulos core
    core_modules = {
        "core/__init__.py": "Módulo core",
        "core/extractor.py": "Extractor de datos de documentos",
        "core/comparador.py": "Comparador de similitud",
        "core/validador.py": "Validador y sistema de scoring"
    }
    
    # Utilidades
    utils = {
        "utils/__init__.py": "Módulo utils",
        "utils/pdf_handler.py": "Manejador de PDFs"
    }
    
    missing_files = []
    
    # Verificar documentación
    print_header("📚 Documentación")
    for file, desc in docs.items():
        if not check_file(file, desc):
            missing_files.append(file)
        print()
    
    # Verificar scripts
    print_header("🔧 Scripts Principales")
    for file, desc in scripts.items():
        if not check_file(file, desc):
            missing_files.append(file)
        print()
    
    # Verificar configuración
    print_header("⚙️  Archivos de Configuración")
    for file, desc in config.items():
        if not check_file(file, desc):
            missing_files.append(file)
        print()
    
    # Verificar módulos core
    print_header("📦 Módulos Core")
    for file, desc in core_modules.items():
        if not check_file(file, desc):
            missing_files.append(file)
        print()
    
    # Verificar utilidades
    print_header("🛠️  Utilidades")
    for file, desc in utils.items():
        if not check_file(file, desc):
            missing_files.append(file)
        print()
    
    # Resumen
    print_header("📊 Resumen de Verificación")
    
    total_files = len(docs) + len(scripts) + len(config) + len(core_modules) + len(utils)
    found_files = total_files - len(missing_files)
    
    print(f"\n  Total de archivos verificados: {total_files}")
    print_colored(f"  ✓ Encontrados: {found_files}", Colors.GREEN)
    
    if missing_files:
        print_colored(f"  ✗ Faltantes: {len(missing_files)}", Colors.RED)
    else:
        print_colored(f"  ✗ Faltantes: 0", Colors.GREEN)
    
    print()
    
    # Resultado final
    if not missing_files:
        print_colored("✅ TODOS LOS ARCHIVOS IMPORTANTES ESTÁN PRESENTES", Colors.GREEN + Colors.BOLD)
        print_colored("   El proyecto está completo y listo para usar\n", Colors.GREEN)
        
        print_colored("📖 Para comenzar:", Colors.CYAN)
        print("   1. Lee INICIO_RAPIDO.md: cat INICIO_RAPIDO.md")
        print("   2. Verifica instalación: python verify_installation.py")
        print("   3. Inicia el servidor: python main.py")
        print()
        
        return 0
    else:
        print_colored("⚠️  ARCHIVOS FALTANTES DETECTADOS", Colors.YELLOW + Colors.BOLD)
        print_colored(f"   {len(missing_files)} archivo(s) no encontrado(s)\n", Colors.YELLOW)
        
        # Sugerir recuperación
        suggest_recovery(missing_files)
        
        print()
        print_colored("📖 Para más ayuda:", Colors.CYAN)
        print("   - Ver: RECUPERAR_ARCHIVOS.md")
        print("   - Ejecutar: python collect_diagnostics.py")
        print()
        
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Verificación cancelada por el usuario")
        sys.exit(130)
    except Exception as e:
        print_colored(f"\n❌ Error durante la verificación: {e}", Colors.RED)
        import traceback
        traceback.print_exc()
        sys.exit(1)
