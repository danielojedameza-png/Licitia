"""Document validation and scoring"""

from typing import Tuple, List, Optional, Dict
from datetime import datetime


class ValidadorEstructural:
    """Validates structural completeness of documents"""
    
    def validar_certificado(self, datos_cert: Dict) -> Tuple[int, List[str]]:
        """Validate certificate data completeness"""
        puntos = 0
        alertas = []
        
        # NIT validation (5 points)
        if datos_cert.get('nit'):
            puntos += 5
        else:
            alertas.append("NIT no identificado")
        
        # Company name validation (5 points)
        if datos_cert.get('razon_social'):
            puntos += 5
        else:
            alertas.append("Razón social no identificada")
        
        # Business object validation (10 points)
        if datos_cert.get('objeto_social') and len(datos_cert.get('objeto_social', '')) > 50:
            puntos += 10
        else:
            alertas.append("Objeto social incompleto o ausente")
        
        # Legal representative (5 points)
        if datos_cert.get('representante_legal'):
            puntos += 5
        else:
            alertas.append("Representante legal no identificado")
        
        # Expedition date validation (5 points)
        fecha_exp = datos_cert.get('fecha_expedicion')
        if fecha_exp:
            puntos += 5
            # Check if expired (more than 90 days)
            try:
                if isinstance(fecha_exp, str):
                    # Try to parse date
                    partes = fecha_exp.split('/')
                    if len(partes) == 3:
                        dia, mes, anio = int(partes[0]), int(partes[1]), int(partes[2])
                        fecha_dt = datetime(anio, mes, dia)
                        dias_desde = (datetime.now() - fecha_dt).days
                        if dias_desde > 90:
                            alertas.append(f"Certificado muy antiguo ({dias_desde} días). Renovar.")
            except:
                pass
        else:
            alertas.append("No se pudo verificar fecha de expedición")
        
        # Status validation (5 points)
        estado = datos_cert.get('estado', 'DESCONOCIDO')
        if estado == 'ACTIVO':
            puntos += 5
        elif estado == 'INACTIVO':
            alertas.append("CRÍTICO: Certificado INACTIVO o empresa disuelta")
        else:
            alertas.append("Estado no activo o no verificado")
        
        # Secondary activities (5 points bonus)
        if datos_cert.get('actividades_secundarias'):
            puntos += 5
        
        return puntos, alertas
    
    def validar_rut(self, datos_rut: Dict) -> Tuple[int, List[str]]:
        """Validate RUT data completeness"""
        puntos = 0
        alertas = []
        
        # NIT validation (3 points)
        if datos_rut.get('nit'):
            puntos += 3
        else:
            alertas.append("RUT: NIT no identificado")
        
        # Company name (2 points)
        if datos_rut.get('razon_social'):
            puntos += 2
        else:
            alertas.append("RUT: Razón social no identificada")
        
        # Economic activity (3 points)
        if datos_rut.get('actividad_economica'):
            puntos += 3
        else:
            alertas.append("RUT: Actividad económica no identificada")
        
        # Status validation (2 points)
        estado = datos_rut.get('estado', 'DESCONOCIDO')
        if estado == 'ACTIVO':
            puntos += 2
        elif estado == 'INACTIVO':
            alertas.append("CRÍTICO: RUT INACTIVO")
        else:
            alertas.append("Falta fecha de expedición")
        
        return puntos, alertas


class ValidadorFinanciero:
    """Validates financial capacity"""
    
    def validar_capacidad(
        self,
        activos: Optional[float],
        valor_proceso: Optional[float],
        porcentaje_minimo: float = 0.10,
        patrimonio: Optional[float] = None
    ) -> Tuple[int, Optional[str]]:
        """
        Validate financial capacity.
        
        Args:
            activos: Total assets
            valor_proceso: Process value
            porcentaje_minimo: Minimum required percentage (default 10%)
            patrimonio: Net equity (optional)
            
        Returns:
            Tuple of (points, alert_message)
        """
        if not activos or not valor_proceso:
            return 10, "No se pudo validar capacidad financiera (falta información)"
        
        minimo_requerido_activos = valor_proceso * porcentaje_minimo
        ratio_activos = activos / minimo_requerido_activos
        
        # Calculate score based on assets
        if ratio_activos >= 1.0:
            puntos = 20
            alerta = None
        elif ratio_activos >= 0.75:
            puntos = 15
            alerta = f"Activos por debajo del mínimo ({ratio_activos*100:.0f}%). Considera consorcio."
        elif ratio_activos >= 0.50:
            puntos = 8
            alerta = f"Activos insuficientes ({ratio_activos*100:.0f}%). Requiere consorcio."
        else:
            puntos = 0
            alerta = f"CRÍTICO: Activos muy insuficientes ({ratio_activos*100:.0f}%). Consorcio necesario."
        
        # Additional check for net equity if provided
        if patrimonio and alerta:
            minimo_requerido_patrimonio = valor_proceso * (porcentaje_minimo / 2)  # 5%
            ratio_patrimonio = patrimonio / minimo_requerido_patrimonio
            if ratio_patrimonio < 1.0:
                alerta += f" Patrimonio insuficiente ({ratio_patrimonio*100:.0f}%)."
        
        return puntos, alerta


class CalculadorScore:
    """Calculates overall score"""
    
    def calcular(
        self,
        puntos_estructura: int,
        puntos_encaje: int,
        puntos_financiero: int
    ) -> Dict:
        """
        Calculate total score with breakdown.
        
        Args:
            puntos_estructura: Points for structural validation (max 40)
            puntos_encaje: Points for business fit (max 40)
            puntos_financiero: Points for financial capacity (max 20)
            
        Returns:
            Dictionary with score details
        """
        score_total = puntos_estructura + puntos_encaje + puntos_financiero
        
        return {
            'score_total': score_total,
            'score_estructura': puntos_estructura,
            'score_encaje': puntos_encaje,
            'score_financiero': puntos_financiero,
            'porcentaje_estructura': (puntos_estructura / 40) * 100,
            'porcentaje_encaje': (puntos_encaje / 40) * 100,
            'porcentaje_financiero': (puntos_financiero / 20) * 100,
        }


class DeterminadorSemaforo:
    """Determines traffic light status based on score and alerts"""
    
    def determinar(
        self,
        score: int,
        alertas: List[str],
        similitud: float
    ) -> str:
        """
        Determine traffic light status.
        
        Args:
            score: Total score (0-100)
            alertas: List of alert messages
            similitud: Similarity score (0-1)
            
        Returns:
            Status: 'VERDE', 'AMARILLO', or 'ROJO'
        """
        # Count critical alerts
        alertas_criticas = len([a for a in alertas if 'CRÍTICO' in a or 'CRITICO' in a])
        
        # Red light conditions
        if alertas_criticas > 0:
            return 'ROJO'
        if score < 40:
            return 'ROJO'
        if similitud < 0.20:
            return 'ROJO'
        
        # Green light conditions
        if score >= 70 and similitud >= 0.50 and len(alertas) <= 2:
            return 'VERDE'
        
        # Default to yellow
        return 'AMARILLO'


class GeneradorRecomendaciones:
    """Generates recommendations based on analysis"""
    
    def generar(
        self,
        semaforo: str,
        score: int,
        similitud: float,
        faltantes: List[str],
        alertas: List[str]
    ) -> str:
        """
        Generate recommendation message.
        
        Args:
            semaforo: Traffic light status
            score: Total score
            similitud: Similarity score
            faltantes: List of missing items
            alertas: List of alerts
            
        Returns:
            Recommendation message
        """
        recomendacion = ""
        
        # Critical issues first
        alertas_criticas = [a for a in alertas if 'CRÍTICO' in a or 'CRITICO' in a]
        if alertas_criticas:
            recomendacion = f"Problemas críticos: {alertas_criticas[0]}. Debes corregir ANTES de aplicar."
            return recomendacion
        
        # Score-based recommendations
        if semaforo == 'VERDE':
            recomendacion = f"¡Excelente! Score: {score}/100. Alta probabilidad de éxito."
            if similitud >= 0.7:
                recomendacion += " Coincidencia perfecta con el objeto del contrato."
            if faltantes:
                recomendacion += f" Completa: {', '.join(faltantes[:2])}."
        
        elif semaforo == 'AMARILLO':
            recomendacion = f"Viable con ajustes. Score: {score}/100."
            if similitud < 0.5:
                recomendacion += f" Coincidencia moderada ({similitud*100:.0f}%)."
                recomendacion += " Refuerza tu propuesta con experiencia certificada."
            if len(faltantes) > 0:
                recomendacion += f" Pendientes: {len(faltantes)} requisitos."
        
        else:  # ROJO
            if similitud < 0.3:
                recomendacion = f"Baja coincidencia ({similitud*100:.0f}%). "
                recomendacion += "Considera: (1) actualizar objeto social, (2) consorcio, (3) justificación clara."
            elif score < 50:
                recomendacion = f"Score bajo ({score}/100). "
                recomendacion += "Documentos incompletos o vencidos. Actualiza antes de aplicar."
            else:
                recomendacion = "Revisa alertas críticas. No recomendado aplicar sin correcciones."
            
            if faltantes:
                recomendacion += f" Faltan: {len(faltantes)} requisitos esenciales."
        
        return recomendacion
