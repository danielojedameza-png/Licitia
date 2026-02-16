"""Text similarity comparison engine"""

import re
from typing import Tuple, Set
from difflib import SequenceMatcher


class ComparadorTextos:
    """Advanced text similarity comparator"""
    
    STOP_WORDS = {
        'el', 'la', 'de', 'del', 'en', 'y', 'o', 'para', 'con', 'por',
        'su', 'sus', 'un', 'una', 'los', 'las', 'al', 'como', 'desde',
        'entre', 'sin', 'sobre', 'tras', 'durante', 'mediante', 'cual',
        'donde', 'cuando', 'quien', 'que', 'esta', 'este', 'estos',
        'estas', 'ese', 'esa', 'esos', 'esas', 'lo', 'le', 'les',
        'se', 'si', 'no', 'ni', 'ya', 'tambien', 'solo', 'mas',
        'pero', 'sino', 'aunque', 'porque', 'pues', 'asi',
        'tan', 'tanto', 'muy', 'ser', 'estar', 'tener', 'hacer',
        'a', 'ante', 'bajo', 'contra', 'hacia', 'hasta', 'segun'
    }
    
    KEYWORDS_IMPORTANTES = {
        'suministro', 'prestacion', 'construccion', 'consultoria',
        'mantenimiento', 'elaboracion', 'produccion', 'comercializacion',
        'distribucion', 'transporte', 'almacenamiento', 'procesamiento',
        'servicio', 'servicios', 'obra', 'obras', 'proyecto', 'proyectos',
        'gestion', 'administracion', 'asesoria', 'capacitacion',
        'formacion', 'educacion', 'salud', 'alimentos', 'agricola',
        'tecnologia', 'sistemas', 'infraestructura', 'vial', 'civil',
        'pesca', 'pesquero', 'pesquera', 'acuicultura', 'agropecuario',
        'ambiental', 'fortalecimiento', 'cadenas', 'valor', 'comunidades',
        'artesanal', 'piangua', 'marino', 'maritimo', 'natural',
        'capacidad', 'transferencia', 'conocimiento', 'tecnica',
        'buenas', 'comunidad'
    }
    
    def calcular_similitud_completa(self, texto1: str, texto2: str, incluir_detalle: bool = False) -> Tuple[float, dict]:
        """Calculate similarity using multiple algorithms"""
        
        texto1_norm = self._normalizar_texto(texto1)
        texto2_norm = self._normalizar_texto(texto2)
        
        sim_keywords, keywords_comunes = self._similitud_keywords(texto1_norm, texto2_norm)
        sim_secuencia = self._similitud_secuencia(texto1_norm, texto2_norm)
        sim_ngramas = self._similitud_ngramas(texto1_norm, texto2_norm, n=2)
        sim_jaccard = self._similitud_jaccard(texto1_norm, texto2_norm)
        boost_importantes = self._boost_keywords_importantes(texto1_norm, texto2_norm)
        
        similitud_total = (
            sim_keywords * 0.50 +
            sim_secuencia * 0.10 +
            sim_ngramas * 0.20 +
            sim_jaccard * 0.10 +
            boost_importantes * 0.10
        )
        
        detalle = {
            'similitud_total': similitud_total,
            'similitud_keywords': sim_keywords,
            'similitud_secuencia': sim_secuencia,
            'similitud_ngramas': sim_ngramas,
            'similitud_jaccard': sim_jaccard,
            'boost_importantes': boost_importantes,
            'keywords_comunes': keywords_comunes if incluir_detalle else len(keywords_comunes),
            'nivel': self._clasificar_similitud(similitud_total)
        }
        
        return similitud_total, detalle
    
    def comparar_con_contexto(self, objeto_social: str, actividades_secundarias: str, objeto_contrato: str) -> dict:
        """Compare business object + activities vs contract object"""
        
        texto_empresa = f"{objeto_social} {actividades_secundarias}"
        
        similitud_principal, detalle_principal = self.calcular_similitud_completa(
            objeto_social, objeto_contrato, incluir_detalle=True
        )
        
        similitud_completa, detalle_completa = self.calcular_similitud_completa(
            texto_empresa, objeto_contrato, incluir_detalle=True
        )
        
        mejor_similitud = max(similitud_principal, similitud_completa)
        fuente_mejor = 'objeto_social' if similitud_principal >= similitud_completa else 'con_actividades_secundarias'
        
        return {
            'similitud_principal': similitud_principal,
            'similitud_con_secundarias': similitud_completa,
            'mejor_similitud': mejor_similitud,
            'fuente_mejor': fuente_mejor,
            'nivel': self._clasificar_similitud(mejor_similitud),
            'detalle_principal': detalle_principal,
            'detalle_completa': detalle_completa,
            'recomendacion': self._generar_recomendacion(
                similitud_principal, similitud_completa,
                detalle_completa.get('keywords_comunes', set())
            )
        }
    
    def _normalizar_texto(self, texto: str) -> str:
        """Normalize text"""
        if not texto:
            return ""
        texto = texto.lower()
        texto = re.sub(r'[^\w\s]', ' ', texto)
        texto = re.sub(r'\s+', ' ', texto)
        return texto.strip()
    
    def _extraer_palabras(self, texto: str, remover_stopwords: bool = True):
        """Extract words from text"""
        palabras = texto.split()
        
        if remover_stopwords:
            palabras = [p for p in palabras if p not in self.STOP_WORDS and len(p) > 2]
        
        return palabras
    
    def _similitud_keywords(self, texto1: str, texto2: str) -> Tuple[float, Set[str]]:
        """Calculate keyword similarity"""
        palabras1 = set(self._extraer_palabras(texto1))
        palabras2 = set(self._extraer_palabras(texto2))
        
        if not palabras2:
            return 0.0, set()
        
        comunes = palabras1.intersection(palabras2)
        similitud = len(comunes) / len(palabras2)
        
        return min(similitud, 1.0), comunes
    
    def _similitud_secuencia(self, texto1: str, texto2: str) -> float:
        """Calculate sequence similarity"""
        return SequenceMatcher(None, texto1, texto2).ratio()
    
    def _similitud_ngramas(self, texto1: str, texto2: str, n: int = 2) -> float:
        """Calculate n-gram similarity"""
        palabras1 = self._extraer_palabras(texto1)
        palabras2 = self._extraer_palabras(texto2)
        
        if len(palabras2) < n:
            return 0.0
        
        ngramas1 = set(tuple(palabras1[i:i+n]) for i in range(len(palabras1)-n+1))
        ngramas2 = set(tuple(palabras2[i:i+n]) for i in range(len(palabras2)-n+1))
        
        if not ngramas2:
            return 0.0
        
        comunes = ngramas1.intersection(ngramas2)
        return len(comunes) / len(ngramas2)
    
    def _similitud_jaccard(self, texto1: str, texto2: str) -> float:
        """Calculate Jaccard similarity"""
        palabras1 = set(self._extraer_palabras(texto1))
        palabras2 = set(self._extraer_palabras(texto2))
        
        if not palabras1 and not palabras2:
            return 0.0
        
        union = palabras1.union(palabras2)
        if not union:
            return 0.0
        
        interseccion = palabras1.intersection(palabras2)
        return len(interseccion) / len(union)
    
    def _boost_keywords_importantes(self, texto1: str, texto2: str) -> float:
        """Boost score for important keywords"""
        palabras1 = set(self._extraer_palabras(texto1, remover_stopwords=False))
        palabras2 = set(self._extraer_palabras(texto2, remover_stopwords=False))
        
        importantes_en_1 = palabras1.intersection(self.KEYWORDS_IMPORTANTES)
        importantes_en_2 = palabras2.intersection(self.KEYWORDS_IMPORTANTES)
        
        if not importantes_en_2:
            return 0.0
        
        comunes_importantes = importantes_en_1.intersection(importantes_en_2)
        return len(comunes_importantes) / len(importantes_en_2)
    
    def _clasificar_similitud(self, similitud: float) -> str:
        """Classify similarity level"""
        if similitud >= 0.7:
            return 'ALTA'
        elif similitud >= 0.5:
            return 'MEDIA'
        elif similitud >= 0.3:
            return 'BAJA'
        else:
            return 'MUY_BAJA'
    
    def _generar_recomendacion(self, sim_principal: float, sim_completa: float, keywords_comunes: set) -> str:
        """Generate recommendation based on similarity"""
        if sim_principal >= 0.7:
            return "Excelente coincidencia. Tu objeto social cubre bien el objeto del contrato."
        elif sim_principal >= 0.5:
            return "Buena coincidencia. Considera reforzar tu propuesta con experiencia específica."
        elif sim_principal >= 0.3:
            return "Coincidencia moderada. Justifica la relación entre tu objeto social y el contrato."
        else:
            return "Coincidencia baja. Considera actualizar tu objeto social o formar consorcio."
