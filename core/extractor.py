"""Document data extraction for certificates, RUT, and notices"""

import re
from typing import Dict, List, Optional
from datetime import datetime


class ExtractorCertificado:
    """Extracts data from Chamber of Commerce Certificate"""
    
    def extraer(self, texto: str) -> Dict:
        """Extract data from certificate text"""
        texto = self._normalizar_texto(texto)
        
        return {
            'nit': self._extraer_nit(texto),
            'razon_social': self._extraer_razon_social(texto),
            'objeto_social': self._extraer_objeto_social(texto),
            'actividades_secundarias': self._extraer_actividades_secundarias(texto),
            'activos': self._extraer_activos(texto),
            'patrimonio': self._extraer_patrimonio(texto),
            'fecha_expedicion': self._extraer_fecha_expedicion(texto),
            'representante_legal': self._extraer_representante(texto),
            'municipio': self._extraer_municipio(texto),
            'estado': self._determinar_estado(texto)
        }
    
    def _normalizar_texto(self, texto: str) -> str:
        """Normalize text for better extraction"""
        texto = re.sub(r'\n{3,}', '\n\n', texto)
        texto = re.sub(r'[ \t]+', ' ', texto)
        return texto.strip()
    
    def _extraer_nit(self, texto: str) -> Optional[str]:
        """Extract NIT/Tax ID"""
        patrones = [
            r'Nit\s*:\s*(\d{9,10}[-]\d)',
            r'nit[:\s.]+(\d{9,10}[-\s]?\d?)',
            r'n\.?\s*i\.?\s*t\.?[:\s]+(\d{9,10}[-\s]?\d?)',
        ]
        
        for patron in patrones:
            match = re.search(patron, texto, re.IGNORECASE)
            if match:
                nit = match.group(1)
                nit = re.sub(r'\s', '', nit)
                nit = nit.replace('-', '')
                if 9 <= len(nit) <= 11 and nit.isdigit():
                    return nit
        return None
    
    def _extraer_razon_social(self, texto: str) -> Optional[str]:
        """Extract company name"""
        patrones = [
            r'Raz[oó]n\s+Social\s*:\s*(.+?)(?=\s*Sigla)',
            r'denominada\s+(.+?)(?=,\s*Sigla)',
            r'razon\s+social[:\s]+([A-Z][A-Z\s.&\-]+?)(?:\s*NIT|\s*Identificacion)',
        ]
        
        for patron in patrones:
            match = re.search(patron, texto, re.IGNORECASE | re.DOTALL)
            if match:
                razon = match.group(1).strip()
                razon = re.sub(r'\s+', ' ', razon)
                if len(razon) > 10:
                    return razon
        return None
    
    def _extraer_objeto_social(self, texto: str) -> Optional[str]:
        """Extract business purpose"""
        patrones = [
            r'OBJETO SOCIAL\s*(.+?)(?=CAPITAL|DOMICILIO|DURACION|Duración|REPRESENTANTE|Página\s+\d+)',
            r'objeto\s+social[:\s]*(.+?)(?=capital|domicilio|duracion)',
        ]
        
        for patron in patrones:
            match = re.search(patron, texto, re.IGNORECASE | re.DOTALL)
            if match:
                objeto = match.group(1).strip()
                objeto = re.sub(r'\s+', ' ', objeto)
                objeto = re.sub(r'\n+', ' ', objeto)
                if len(objeto) > 50:
                    return objeto
        
        return None
    
    def _extraer_actividades_secundarias(self, texto: str) -> Optional[str]:
        """Extract secondary activities"""
        patrones = [
            r'actividad(?:es)?\s+secundaria(?:s)?[:\s]+(.{50,500}?)(?=\n\s*[A-Z])',
            r'otras\s+actividades[:\s]+(.{50,500}?)(?=\n\s*[A-Z])',
        ]
        
        for patron in patrones:
            match = re.search(patron, texto, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:500]
        
        return None
    
    def _extraer_activos(self, texto: str) -> Optional[float]:
        """Extract assets value"""
        patrones = [
            r'activos?\s+totales?[:\s]+\$?\s*([\d.,]+)',
            r'total\s+activos?[:\s]+\$?\s*([\d.,]+)',
            r'activos?[:\s]+\$?\s*([\d.,]+)',
        ]
        
        for patron in patrones:
            match = re.search(patron, texto, re.IGNORECASE)
            if match:
                valor = self._parsear_valor_monetario(match.group(1))
                if valor and valor > 0:
                    return valor
        return None
    
    def _extraer_patrimonio(self, texto: str) -> Optional[float]:
        """Extract equity value"""
        patrones = [
            r'patrimonio[:\s]+\$?\s*([\d.,]+)',
            r'capital[:\s]+\$?\s*([\d.,]+)',
        ]
        
        for patron in patrones:
            match = re.search(patron, texto, re.IGNORECASE)
            if match:
                valor = self._parsear_valor_monetario(match.group(1))
                if valor and valor > 0:
                    return valor
        return None
    
    def _extraer_fecha_expedicion(self, texto: str) -> Optional[str]:
        """Extract expedition date"""
        patrones = [
            r'(?:Fecha\s+)?expedici[oó]n[:\s]+(\d{1,2})[/\-](\d{1,2})[/\-](\d{4})',
            r'(?:fecha|date)[:\s]+(\d{1,2})[/\-](\d{1,2})[/\-](\d{4})',
        ]
        
        for patron in patrones:
            match = re.search(patron, texto, re.IGNORECASE)
            if match:
                try:
                    dia = int(match.group(1))
                    mes = int(match.group(2))
                    anio = int(match.group(3))
                    return f"{dia:02d}/{mes:02d}/{anio}"
                except:
                    pass
        
        return None
    
    def _extraer_representante(self, texto: str) -> Optional[str]:
        """Extract legal representative"""
        patrones = [
            r'representante\s+legal[:\s]+([A-Z][A-Z\s.]+?)(?=\n|Identificacion|CC|FECHA)',
            r'gerente[:\s]+([A-Z][A-Z\s.]+?)(?=\n|Identificacion)',
        ]
        
        for patron in patrones:
            match = re.search(patron, texto, re.IGNORECASE)
            if match:
                nombre = match.group(1).strip()
                nombre = re.sub(r'\s+', ' ', nombre)
                if 5 < len(nombre) < 80:
                    return nombre
        
        return None
    
    def _extraer_municipio(self, texto: str) -> Optional[str]:
        """Extract municipality"""
        patrones = [
            r'(?:Municipio|Domicilio)[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
            r'municipio[:\s]+([A-Z][a-z]+)',
            r'domicilio[:\s]+([A-Z][a-z]+)',
        ]
        
        for patron in patrones:
            match = re.search(patron, texto, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _determinar_estado(self, texto: str) -> str:
        """Determine certificate status"""
        texto_lower = texto.lower()
        
        if re.search(r'ultimo\s+a[ñn]o\s+renovado\s*:\s*202[0-9]', texto_lower):
            return 'ACTIVO'
        if re.search(r'fecha\s+de\s+renovaci[oó]n\s*:\s*\d{1,2}\s+de\s+\w+\s+de\s+202[0-9]', texto_lower):
            return 'ACTIVO'
        
        if re.search(r'estado\s*:\s*inactiv', texto_lower):
            return 'INACTIVO'
        if re.search(r'entidad\s+(cancelad|liquidad|disuelt)', texto_lower):
            return 'INACTIVO'
        if re.search(r'(cancelad|liquidad|disuelt)[oa]\s+el\s+\d', texto_lower):
            return 'INACTIVO'
        
        if re.search(r'estado\s*:\s*activ', texto_lower):
            return 'ACTIVO'
        if re.search(r'\bvigente\b', texto_lower):
            return 'ACTIVO'
        
        return 'DESCONOCIDO'
    
    def _parsear_valor_monetario(self, valor_str: str) -> Optional[float]:
        """Parse monetary value from string"""
        try:
            valor_limpio = valor_str.replace('.', '').replace(',', '')
            valor = float(valor_limpio)
            if 100 <= valor <= 1000000000000:
                return valor
        except:
            pass
        return None


class ExtractorRUT:
    """Extracts data from RUT (Tax Registration)"""
    
    def extraer(self, texto: str) -> Dict:
        """Extract data from RUT text"""
        return {
            'nit': self._extraer_nit(texto),
            'razon_social': self._extraer_razon_social(texto),
            'actividad_economica': self._extraer_actividad(texto),
            'estado': self._determinar_estado(texto)
        }
    
    def _extraer_nit(self, texto: str) -> Optional[str]:
        """Extract NIT"""
        patron = r'(?:NIT|Nit)[:\s]+(\d{9,10}[-]?\d?)'
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            nit = match.group(1).replace('-', '').replace(' ', '')
            if nit.isdigit():
                return nit
        return None
    
    def _extraer_razon_social(self, texto: str) -> Optional[str]:
        """Extract company name from RUT"""
        patron = r'(?:RAZON SOCIAL|Razon Social)[:\s]+(.+?)(?=\n|ACTIVIDAD)'
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None
    
    def _extraer_actividad(self, texto: str) -> Optional[str]:
        """Extract economic activity"""
        patron = r'ACTIVIDAD ECONOMICA[:\s]+(.{10,200})'
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            return match.group(1).strip()[:200]
        return None
    
    def _determinar_estado(self, texto: str) -> str:
        """Determine RUT status"""
        if re.search(r'estado[:\s]+activ', texto, re.IGNORECASE):
            return 'ACTIVO'
        if re.search(r'estado[:\s]+inactiv', texto, re.IGNORECASE):
            return 'INACTIVO'
        return 'DESCONOCIDO'


class ExtractorAviso:
    """Extracts data from tender notice"""
    
    def extraer(self, texto: str) -> Dict:
        """Extract data from tender notice text"""
        return {
            'numero_proceso': self._extraer_numero_proceso(texto),
            'entidad': self._extraer_entidad(texto),
            'objeto_contrato': self._extraer_objeto(texto),
            'descripcion': self._extraer_descripcion(texto),
            'valor_estimado': self._extraer_valor(texto),
            'plazo': self._extraer_plazo(texto),
            'requisitos_mencionados': self._extraer_requisitos(texto)
        }
    
    def _extraer_numero_proceso(self, texto: str) -> Optional[str]:
        """Extract process number"""
        patrones = [
            r'proceso[:\s]+([A-Z0-9\-]+)',
            r'numero\s+proceso[:\s]+([A-Z0-9\-]+)',
        ]
        
        for patron in patrones:
            match = re.search(patron, texto, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extraer_entidad(self, texto: str) -> Optional[str]:
        """Extract contracting entity"""
        patrones = [
            r'entidad[:\s]+([A-Z][A-Z\s.]+?)(?:\n|NIT)',
            r'contratante[:\s]+([A-Z][A-Z\s.]+?)(?:\n|NIT)',
        ]
        
        for patron in patrones:
            match = re.search(patron, texto, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extraer_objeto(self, texto: str) -> Optional[str]:
        """Extract contract object"""
        patrones = [
            r'objeto\s+del?\s+contrat[oa][:\s]+(.{50,1500}?)(?=\n\s*(?:descripcion|valor|plazo|condiciones|requisitos|alcance|modalidad))',
            r'objeto\s+de\s+la\s+contratacion[:\s]+(.{50,1500}?)(?=\n\s*(?:descripcion|valor|plazo|condiciones|requisitos|alcance|modalidad))',
            r'contratar\s+la\s+\w+\s+(.{50,1500}?)(?=\n\s*(?:alcance|descripcion|valor|plazo|condiciones|requisitos|modalidad))',
            r'objeto[:\s]+(.{50,1500}?)(?=\n\s*(?:descripcion|valor|plazo|condiciones|requisitos|alcance|modalidad))',
        ]
        
        for patron in patrones:
            match = re.search(patron, texto, re.IGNORECASE | re.DOTALL)
            if match:
                objeto = match.group(1).strip()
                objeto = re.sub(r'\s+', ' ', objeto)
                if len(objeto) > 30:
                    return objeto[:1500]
        
        # Buscar "contratar" sin contexto previo
        match_contratar = re.search(r'contratar\s+la\s+\w+\s+(.{50,1500}?)(?=\n\s*[A-Z]|\Z)', texto, re.IGNORECASE | re.DOTALL)
        if match_contratar:
            return match_contratar.group(0).strip()[:1500]
        
        return None
    
    def _extraer_descripcion(self, texto: str) -> Optional[str]:
        """Extract description"""
        patron = r'descripcion[:\s]+(.{50,500}?)(?=\n\s*[A-Z]|\Z)'
        match = re.search(patron, texto, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()[:500]
        return None
    
    def _extraer_valor(self, texto: str) -> Optional[float]:
        """Extract estimated value"""
        patrones = [
            r'(?:presupuesto|valor)\s+(?:oficial|estimado)[:\s]+\$?\s*([\d.,]+)',
            r'cuantia[:\s]+\$?\s*([\d.,]+)',
        ]
        
        for patron in patrones:
            match = re.search(patron, texto, re.IGNORECASE)
            if match:
                valor_str = match.group(1).replace('.', '').replace(',', '')
                try:
                    valor = float(valor_str)
                    if 1000000 <= valor <= 100000000000:
                        return valor
                except:
                    continue
        
        return None
    
    def _extraer_plazo(self, texto: str) -> Optional[str]:
        """Extract contract duration"""
        patron = r'plazo[:\s]+(.{5,100}?)(?=\n|$)'
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            return match.group(1).strip()[:100]
        return None
    
    def _extraer_requisitos(self, texto: str) -> List[str]:
        """Extract mentioned requirements"""
        requisitos = []
        palabras_clave = ['RUP', 'RUT', 'certificado', 'poliza', 'experiencia', 'estados financieros']
        
        texto_lower = texto.lower()
        for req in palabras_clave:
            if req.lower() in texto_lower:
                requisitos.append(req)
        
        return requisitos
