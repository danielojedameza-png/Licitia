"""
Main DEMO analysis engine
Professional version without AI
"""

from datetime import datetime
from typing import Dict, Optional

# Local imports
try:
    from core.extractor import ExtractorCertificado, ExtractorRUT, ExtractorAviso
    from core.comparador import ComparadorTextos
    from core.validador import (
        ValidadorEstructural, ValidadorFinanciero,
        CalculadorScore, DeterminadorSemaforo, GeneradorRecomendaciones
    )
    MODULOS_COMPLETOS = True
except ImportError:
    MODULOS_COMPLETOS = False


class DemoEngine:
    """Main DEMO analysis engine"""
    
    def __init__(self):
        if MODULOS_COMPLETOS:
            self.extractor_cert = ExtractorCertificado()
            self.extractor_rut = ExtractorRUT()
            self.extractor_aviso = ExtractorAviso()
            self.comparador = ComparadorTextos()
            self.validador_estructural = ValidadorEstructural()
            self.validador_financiero = ValidadorFinanciero()
            self.calculador_score = CalculadorScore()
            self.determinador_semaforo = DeterminadorSemaforo()
            self.generador_recomendaciones = GeneradorRecomendaciones()
    
    def analizar(
        self,
        certificado_texto: str,
        rut_texto: str,
        aviso_texto: str,
        valor_proceso: Optional[float] = None
    ) -> Dict:
        """
        Complete professional analysis.
        
        Args:
            certificado_texto: Certificate text
            rut_texto: RUT text
            aviso_texto: Tender notice text
            valor_proceso: Optional process value
            
        Returns:
            Complete analysis results
        """
        
        timestamp_inicio = datetime.now()
        
        if not MODULOS_COMPLETOS:
            # Fallback to basic analysis
            return self._analisis_basico(
                certificado_texto, rut_texto, aviso_texto, valor_proceso
            )
        
        # === STEP 1: DATA EXTRACTION ===
        datos_cert = self.extractor_cert.extraer(certificado_texto)
        datos_rut = self.extractor_rut.extraer(rut_texto)
        datos_aviso = self.extractor_aviso.extraer(aviso_texto)
        
        # If value not provided, try to extract from notice
        if not valor_proceso:
            valor_proceso = datos_aviso.get('valor_estimado')
        
        # === STEP 2: STRUCTURAL VALIDATION ===
        puntos_cert, alertas_cert = self.validador_estructural.validar_certificado(datos_cert)
        puntos_rut, alertas_rut = self.validador_estructural.validar_rut(datos_rut)
        
        puntos_estructura = puntos_cert + puntos_rut
        alertas_estructura = alertas_cert + alertas_rut
        
        # === STEP 3: SIMILARITY COMPARISON ===
        similitud_resultado = self.comparador.comparar_con_contexto(
            datos_cert.get('objeto_social', ''),
            datos_cert.get('actividades_secundarias', ''),
            datos_aviso.get('objeto_contrato', '')
        )
        
        similitud = similitud_resultado['mejor_similitud']
        puntos_encaje = int(similitud * 40)
        
        # === STEP 4: FINANCIAL VALIDATION ===
        puntos_financiero, alerta_financiera = self.validador_financiero.validar_capacidad(
            datos_cert.get('activos'),
            valor_proceso,
            patrimonio=datos_cert.get('patrimonio')
        )
        
        alertas_financieras = [alerta_financiera] if alerta_financiera else []
        
        # === STEP 5: SCORE CALCULATION ===
        score_detalle = self.calculador_score.calcular(
            puntos_estructura,
            puntos_encaje,
            puntos_financiero
        )
        
        score_total = score_detalle['score_total']
        
        # === STEP 6: IDENTIFY MISSING ITEMS ===
        faltantes = self._identificar_faltantes_simple(
            datos_cert, datos_rut, datos_aviso, alertas_estructura
        )
        
        # === STEP 7: DETERMINE TRAFFIC LIGHT ===
        todas_alertas = alertas_estructura + alertas_financieras
        semaforo = self.determinador_semaforo.determinar(
            score_total, todas_alertas, similitud
        )
        
        # === STEP 8: GENERATE RECOMMENDATION ===
        recomendacion = self.generador_recomendaciones.generar(
            semaforo, score_total, similitud, faltantes, todas_alertas
        )
        
        # === RESULT ===
        timestamp_fin = datetime.now()
        tiempo_procesamiento = (timestamp_fin - timestamp_inicio).total_seconds()
        
        return {
            'semaforo': semaforo,
            'score': score_total,
            'similitud': similitud,
            'recomendacion': recomendacion,
            'faltantes': faltantes[:5],
            'alertas': todas_alertas,
            'score_detalle': score_detalle,
            'analisis_similitud': {
                'similitud_principal': similitud_resultado.get('similitud_principal', similitud),
                'nivel': similitud_resultado.get('nivel', 'DESCONOCIDO'),
                'recomendacion_similitud': similitud_resultado.get('recomendacion', '')
            },
            'datos_extraidos': {
                'nit': datos_cert.get('nit'),
                'razon_social': datos_cert.get('razon_social'),
                'activos': datos_cert.get('activos'),
                'estado_certificado': datos_cert.get('estado'),
                'estado_rut': datos_rut.get('estado'),
                'valor_proceso': valor_proceso
            },
            'metadata': {
                'timestamp': timestamp_fin.isoformat(),
                'tiempo_procesamiento_segundos': round(tiempo_procesamiento, 2),
                'version': '2.0.0',
                'tipo_analisis': 'DEMO_PROFESIONAL',
                'costo_tokens': 0
            }
        }
    
    def _analisis_basico(self, certificado_texto, rut_texto, aviso_texto, valor_proceso):
        """Basic analysis if complete modules are not available"""
        score = 60
        
        if "activo" in rut_texto.lower():
            score += 10
        
        if "vigente" in certificado_texto.lower() or "renovado" in certificado_texto.lower():
            score += 10
        
        palabras_aviso = set(aviso_texto.lower().split())
        palabras_cert = set(certificado_texto.lower().split())
        comunes = palabras_aviso.intersection(palabras_cert)
        similitud = len(comunes) / len(palabras_aviso) if palabras_aviso else 0
        
        if similitud > 0.3:
            score += 10
        
        if score >= 70:
            semaforo = 'VERDE'
        elif score >= 50:
            semaforo = 'AMARILLO'
        else:
            semaforo = 'ROJO'
        
        return {
            'semaforo': semaforo,
            'score': min(score, 100),
            'similitud': similitud,
            'recomendacion': f'Score: {score}/100. Análisis básico (módulos completos pendientes).',
            'faltantes': ['Validación completa pendiente'],
            'alertas': [],
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'tipo_analisis': 'DEMO_BASICO',
                'costo_tokens': 0
            }
        }
    
    def _identificar_faltantes_simple(self, datos_cert, datos_rut, datos_aviso, alertas):
        """Simple identification of missing items"""
        faltantes = []
        
        # Missing items from critical alerts
        for alerta in alertas:
            if 'CRÍTICO' in alerta or 'vencido' in alerta.lower():
                if 'Certificado' in alerta:
                    faltantes.append("Certificado de Cámara actualizado (menos de 30 días)")
                elif 'RUT' in alerta:
                    faltantes.append("RUT actualizado")
        
        # Missing items from absent data
        if not datos_cert.get('activos'):
            faltantes.append("Activos no identificados en certificado")
        
        if not datos_cert.get('representante_legal'):
            faltantes.append("Representante legal no identificado")
        
        # Common missing items in tenders
        if not faltantes:
            faltantes = [
                "RUP actualizado con experiencia certificada",
                "Pólizas requeridas según el pliego",
                "Estados financieros con revisor fiscal"
            ]
        
        return faltantes


def generar_mensaje_whatsapp(resultado: Dict) -> str:
    """Generate professional WhatsApp message"""
    
    emoji_semaforo = {'VERDE': '🟢', 'AMARILLO': '🟡', 'ROJO': '🔴'}
    emoji = emoji_semaforo.get(resultado['semaforo'], '⚪')
    
    mensaje = f"""🎯 RESULTADO ANÁLISIS DEMO

{emoji} {resultado['semaforo']}
Score: {resultado['score']}/100

📊 Desglose:
"""
    
    # Add breakdown if it exists
    if 'score_detalle' in resultado:
        detalle = resultado['score_detalle']
        mensaje += f"""• Documentos: {detalle.get('score_estructura', 0)}/40
• Encaje objeto: {detalle.get('score_encaje', 0)}/40
• Capacidad financiera: {detalle.get('score_financiero', 0)}/20

"""
    
    # Similarity
    mensaje += f"🎯 Similitud objeto social: {resultado['similitud']*100:.0f}%\n\n"
    
    # Missing items
    if resultado.get('faltantes'):
        mensaje += f"⚠️ TOP {len(resultado['faltantes'])} FALTANTES:\n"
        for i, faltante in enumerate(resultado['faltantes'][:3], 1):
            mensaje += f"{i}. {faltante}\n"
        mensaje += "\n"
    
    # Critical alerts
    alertas_criticas = [a for a in resultado.get('alertas', []) if 'CRÍTICO' in a]
    if alertas_criticas:
        mensaje += "🚨 ALERTAS CRÍTICAS:\n"
        for alerta in alertas_criticas[:2]:
            mensaje += f"• {alerta}\n"
        mensaje += "\n"
    
    # Recommendation
    mensaje += f"💡 RECOMENDACIÓN:\n{resultado['recomendacion']}\n\n"
    
    # CTA
    mensaje += """────────────────────────

⚡ Análisis DEMO (sin IA)
Precisión: 75-80%

¿Quieres análisis PRO con IA?
✓ Validación experta
✓ Análisis financiero detallado
✓ Plan de acción completo
✓ Soporte 24h

💰 Desde $20.000

Responde SÍ para cotizar"""
    
    return mensaje
