#!/usr/bin/env python3
"""
Script de prueba rápida para LicitIA

Ejecuta pruebas básicas de los endpoints principales y genera un reporte.
"""

import sys
import requests
import json
import time
from datetime import datetime
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
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text:^60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓{Colors.END} {text}")

def print_error(text):
    print(f"{Colors.RED}✗{Colors.END} {text}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠{Colors.END} {text}")

def print_info(text):
    print(f"  {text}")

class APITester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.results = []
        self.start_time = None
    
    def start(self):
        self.start_time = time.time()
        print_header("LicitIA - Prueba Rápida de API")
        print_info(f"URL Base: {self.base_url}")
        print_info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    def test_endpoint(self, name, method, endpoint, data=None, expected_status=200):
        """Prueba un endpoint y registra el resultado"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            print_info(f"Probando: {method} {endpoint}")
            
            start = time.time()
            
            if method == "GET":
                response = requests.get(url, timeout=10)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=10)
            else:
                raise ValueError(f"Método no soportado: {method}")
            
            elapsed = time.time() - start
            
            success = response.status_code == expected_status
            
            result = {
                "name": name,
                "method": method,
                "endpoint": endpoint,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "success": success,
                "response_time": elapsed,
                "response_size": len(response.content),
            }
            
            if success:
                print_success(f"{name} - OK ({elapsed:.2f}s)")
                try:
                    result["response_preview"] = str(response.json())[:100]
                except:
                    result["response_preview"] = str(response.text)[:100]
            else:
                print_error(f"{name} - FALLÓ (Status: {response.status_code})")
                result["error"] = response.text[:200]
            
            self.results.append(result)
            return success
            
        except requests.exceptions.ConnectionError:
            print_error(f"{name} - No se pudo conectar al servidor")
            self.results.append({
                "name": name,
                "success": False,
                "error": "Connection refused - ¿Está el servidor corriendo?"
            })
            return False
            
        except requests.exceptions.Timeout:
            print_error(f"{name} - Timeout")
            self.results.append({
                "name": name,
                "success": False,
                "error": "Request timeout"
            })
            return False
            
        except Exception as e:
            print_error(f"{name} - Error: {str(e)}")
            self.results.append({
                "name": name,
                "success": False,
                "error": str(e)
            })
            return False
    
    def run_tests(self):
        """Ejecuta todas las pruebas"""
        
        # Test 1: Health Check
        print_header("1. Health Check")
        self.test_endpoint(
            "Root Endpoint",
            "GET",
            "/"
        )
        
        self.test_endpoint(
            "Pricing Health",
            "GET",
            "/api/pricing/health"
        )
        
        self.test_endpoint(
            "Analysis Health",
            "GET",
            "/api/analysis/health"
        )
        
        # Test 2: Subscription Plans
        print_header("2. Planes de Suscripción")
        self.test_endpoint(
            "Get Subscriptions",
            "GET",
            "/api/pricing/subscriptions"
        )
        
        # Test 3: PLUS Pricing
        print_header("3. Cálculo de Precio PLUS")
        self.test_endpoint(
            "PLUS - Caso Normal",
            "POST",
            "/api/pricing/plus",
            {
                "assets": 500000000,
                "process_value": 100000000
            }
        )
        
        self.test_endpoint(
            "PLUS - Con Usuario Social",
            "POST",
            "/api/pricing/plus",
            {
                "assets": 150000000,
                "process_value": 80000000,
                "user_type": "productor"
            }
        )
        
        # Test 4: PRO Pricing
        print_header("4. Cálculo de Precio PRO")
        self.test_endpoint(
            "PRO - Caso Normal",
            "POST",
            "/api/pricing/pro",
            {
                "assets": 500000000,
                "process_value": 300000000,
                "num_annexes": 8
            }
        )
        
        self.test_endpoint(
            "PRO - Con Anexos Extra",
            "POST",
            "/api/pricing/pro",
            {
                "assets": 800000000,
                "process_value": 500000000,
                "num_annexes": 15
            }
        )
        
        # Test 5: Complete Quote
        print_header("5. Cotización Completa")
        self.test_endpoint(
            "Complete Quote",
            "POST",
            "/api/pricing/quote",
            {
                "assets": 600000000,
                "process_value": 250000000,
                "num_annexes": 10,
                "user_type": "empresa"
            }
        )
        
        # Test 6: Capped Mode
        print_header("6. Modo Capeado (20-80K)")
        self.test_endpoint(
            "PLUS Capped",
            "POST",
            "/api/pricing/plus",
            {
                "assets": 1000000000,
                "process_value": 500000000,
                "pricing_mode": "capped"
            }
        )
        
        # Test 7: Package Discounts
        print_header("7. Descuentos por Paquete")
        self.test_endpoint(
            "Package Discount 3",
            "POST",
            "/api/pricing/package-discount",
            {
                "service_type": "PRO",
                "num_processes": 3
            }
        )
    
    def print_summary(self):
        """Imprime resumen de resultados"""
        print_header("RESUMEN DE PRUEBAS")
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r.get("success"))
        failed = total - passed
        
        print_info(f"Total de pruebas: {total}")
        print_success(f"Exitosas: {passed}")
        if failed > 0:
            print_error(f"Fallidas: {failed}")
        else:
            print_info(f"Fallidas: 0")
        
        elapsed = time.time() - self.start_time
        print_info(f"Tiempo total: {elapsed:.2f}s")
        
        # Mostrar tests fallidos
        failed_tests = [r for r in self.results if not r.get("success")]
        if failed_tests:
            print("\n" + Colors.RED + "Tests Fallidos:" + Colors.END)
            for test in failed_tests:
                print_error(f"  - {test['name']}: {test.get('error', 'Unknown error')}")
        
        # Estadísticas de rendimiento
        successful_tests = [r for r in self.results if r.get("success") and "response_time" in r]
        if successful_tests:
            avg_time = sum(r["response_time"] for r in successful_tests) / len(successful_tests)
            max_time = max(r["response_time"] for r in successful_tests)
            min_time = min(r["response_time"] for r in successful_tests)
            
            print("\n" + Colors.BLUE + "Estadísticas de Rendimiento:" + Colors.END)
            print_info(f"Tiempo promedio: {avg_time:.3f}s")
            print_info(f"Tiempo máximo: {max_time:.3f}s")
            print_info(f"Tiempo mínimo: {min_time:.3f}s")
        
        # Resultado final
        print("\n" + "="*60)
        if failed == 0:
            print(f"{Colors.GREEN}{Colors.BOLD}✓ TODAS LAS PRUEBAS PASARON{Colors.END}")
            print_info("El sistema está funcionando correctamente")
        else:
            print(f"{Colors.YELLOW}{Colors.BOLD}⚠ ALGUNAS PRUEBAS FALLARON{Colors.END}")
            print_info("Revisa los errores arriba")
            print_info("Tip: Asegúrate de que el servidor esté corriendo:")
            print_info("  python main.py")
        print("="*60 + "\n")
        
        return failed == 0
    
    def save_report(self, filename=None):
        """Guarda reporte en archivo JSON"""
        if filename is None:
            filename = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "base_url": self.base_url,
            "total_tests": len(self.results),
            "passed": sum(1 for r in self.results if r.get("success")),
            "failed": sum(1 for r in self.results if not r.get("success")),
            "total_time": time.time() - self.start_time,
            "tests": self.results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print_info(f"Reporte guardado en: {filename}")

def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Prueba rápida de API de LicitIA')
    parser.add_argument(
        '--url',
        default='http://localhost:8000',
        help='URL base del servidor (default: http://localhost:8000)'
    )
    parser.add_argument(
        '--save-report',
        action='store_true',
        help='Guardar reporte en archivo JSON'
    )
    
    args = parser.parse_args()
    
    tester = APITester(base_url=args.url)
    tester.start()
    
    try:
        tester.run_tests()
        success = tester.print_summary()
        
        if args.save_report:
            tester.save_report()
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Pruebas interrumpidas por el usuario")
        return 1
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {str(e)}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
