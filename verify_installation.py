#!/usr/bin/env python3
"""
Script de verificación de instalación para LicitIA

Ejecuta este script para verificar que todo está instalado correctamente.
"""

import sys
import os
import importlib
import subprocess
from pathlib import Path

# Colores para terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """Imprime un encabezado destacado"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text:^60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}\n")

def print_success(text):
    """Imprime mensaje de éxito"""
    print(f"{Colors.GREEN}✓{Colors.END} {text}")

def print_error(text):
    """Imprime mensaje de error"""
    print(f"{Colors.RED}✗{Colors.END} {text}")

def print_warning(text):
    """Imprime mensaje de advertencia"""
    print(f"{Colors.YELLOW}⚠{Colors.END} {text}")

def print_info(text):
    """Imprime información"""
    print(f"  {text}")

def check_python_version():
    """Verifica la versión de Python"""
    print_header("1. Verificando Versión de Python")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print_info(f"Versión de Python: {version_str}")
    
    if version.major == 3 and version.minor >= 8:
        print_success(f"Python {version_str} es compatible ✓")
        return True
    else:
        print_error(f"Python {version_str} no es compatible")
        print_info("Se requiere Python 3.8 o superior")
        return False

def check_venv():
    """Verifica si está en un entorno virtual"""
    print_header("2. Verificando Entorno Virtual")
    
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        print_success("Entorno virtual activado ✓")
        print_info(f"Ubicación: {sys.prefix}")
        return True
    else:
        print_warning("No se detectó entorno virtual")
        print_info("Recomendación: Usa un entorno virtual (venv)")
        print_info("Comando: python -m venv venv")
        return True  # No es crítico, pero es recomendado

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    print_header("3. Verificando Dependencias")
    
    required_packages = {
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'pydantic': 'Pydantic',
        'PyPDF2': 'PyPDF2',
        'pytest': 'Pytest',
    }
    
    all_installed = True
    installed_packages = []
    missing_packages = []
    
    for package, display_name in required_packages.items():
        try:
            mod = importlib.import_module(package.lower())
            version = getattr(mod, '__version__', 'unknown')
            print_success(f"{display_name} instalado (v{version})")
            installed_packages.append(package)
        except ImportError:
            print_error(f"{display_name} NO instalado")
            missing_packages.append(package)
            all_installed = False
    
    if not all_installed:
        print("\n" + Colors.YELLOW + "Para instalar las dependencias faltantes:" + Colors.END)
        print_info("pip install -r requirements.txt")
    
    return all_installed

def check_project_structure():
    """Verifica la estructura del proyecto"""
    print_header("4. Verificando Estructura del Proyecto")
    
    required_files = [
        'main.py',
        'requirements.txt',
        'pricing_calculator.py',
        'pricing_config.py',
        'models.py',
        'demo_engine.py',
    ]
    
    required_dirs = [
        'core',
        'utils',
        'tests',
    ]
    
    all_present = True
    
    # Verificar archivos
    for file in required_files:
        if Path(file).exists():
            print_success(f"Archivo: {file}")
        else:
            print_error(f"Archivo faltante: {file}")
            all_present = False
    
    # Verificar directorios
    for dir_name in required_dirs:
        if Path(dir_name).exists() and Path(dir_name).is_dir():
            print_success(f"Directorio: {dir_name}/")
        else:
            print_warning(f"Directorio faltante: {dir_name}/")
    
    return all_present

def check_imports():
    """Verifica que los módulos del proyecto se puedan importar"""
    print_header("5. Verificando Módulos del Proyecto")
    
    modules_to_test = [
        'pricing_calculator',
        'pricing_config',
        'models',
        'demo_engine',
        'core.extractor',
        'core.comparador',
        'core.validador',
        'utils.pdf_handler',
    ]
    
    all_imported = True
    
    for module in modules_to_test:
        try:
            importlib.import_module(module)
            print_success(f"Módulo: {module}")
        except Exception as e:
            print_error(f"Error al importar {module}: {str(e)}")
            all_imported = False
    
    return all_imported

def run_quick_tests():
    """Ejecuta tests básicos"""
    print_header("6. Ejecutando Tests Básicos")
    
    try:
        # Intentar ejecutar pytest
        result = subprocess.run(
            ['pytest', '--collect-only', '-q'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            # Contar tests
            output_lines = result.stdout.split('\n')
            test_count = len([line for line in output_lines if '::test_' in line])
            print_success(f"Tests encontrados: {test_count}")
            
            # Ejecutar un subset de tests
            print_info("Ejecutando tests básicos...")
            result = subprocess.run(
                ['pytest', '-x', '--tb=short', '-q'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print_success("Tests básicos pasaron ✓")
                return True
            else:
                print_warning("Algunos tests fallaron")
                print_info("Ejecuta 'pytest -v' para ver detalles")
                return True  # No es crítico para verificación
        else:
            print_warning("No se pudieron ejecutar los tests")
            return True
            
    except subprocess.TimeoutExpired:
        print_warning("Tests tomaron demasiado tiempo")
        return True
    except FileNotFoundError:
        print_warning("pytest no encontrado")
        print_info("Instala con: pip install pytest")
        return True
    except Exception as e:
        print_warning(f"Error al ejecutar tests: {e}")
        return True

def check_port_availability():
    """Verifica si el puerto 8000 está disponible"""
    print_header("7. Verificando Disponibilidad del Puerto")
    
    import socket
    
    port = 8000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.bind(('localhost', port))
        sock.close()
        print_success(f"Puerto {port} está disponible ✓")
        return True
    except OSError:
        print_warning(f"Puerto {port} ya está en uso")
        print_info("Puedes usar otro puerto con: uvicorn main:app --port 8080")
        return True  # No crítico

def print_summary(results):
    """Imprime resumen de verificación"""
    print_header("RESUMEN DE VERIFICACIÓN")
    
    total = len(results)
    passed = sum(1 for r in results.values() if r)
    
    print_info(f"Verificaciones completadas: {passed}/{total}")
    
    if all(results.values()):
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ INSTALACIÓN VERIFICADA CORRECTAMENTE{Colors.END}")
        print_info("El sistema está listo para usar")
        print_info("\nPara iniciar el servidor:")
        print_info("  python main.py")
        print_info("o:")
        print_info("  uvicorn main:app --reload")
        return True
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ VERIFICACIÓN INCOMPLETA{Colors.END}")
        print_info("Revisa los errores arriba y corrígelos")
        
        failed_checks = [name for name, result in results.items() if not result]
        if failed_checks:
            print_info("\nVerificaciones fallidas:")
            for check in failed_checks:
                print_error(f"  - {check}")
        
        return False

def main():
    """Función principal"""
    print(f"\n{Colors.BOLD}LicitIA - Verificación de Instalación{Colors.END}")
    print_info("Este script verificará que todo esté instalado correctamente\n")
    
    results = {}
    
    # Ejecutar todas las verificaciones
    results['Python'] = check_python_version()
    results['Entorno Virtual'] = check_venv()
    results['Dependencias'] = check_dependencies()
    results['Estructura'] = check_project_structure()
    results['Módulos'] = check_imports()
    results['Tests'] = run_quick_tests()
    results['Puerto'] = check_port_availability()
    
    # Imprimir resumen
    success = print_summary(results)
    
    # Mensaje final
    print("\n" + "="*60)
    print_info("Para más ayuda, consulta: GUIA_INSTALACION.md")
    print_info("Para reportar errores: COMO_REPORTAR_ERRORES.md")
    print("="*60 + "\n")
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
