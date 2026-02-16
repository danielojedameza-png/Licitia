"""Tests for extractor module"""

import pytest
from core.extractor import ExtractorCertificado, ExtractorRUT, ExtractorAviso


def test_extractor_certificado():
    """Test certificate extractor"""
    texto = """
    CERTIFICADO DE EXISTENCIA Y REPRESENTACION LEGAL
    NIT: 8060130247
    Razón Social: ASOCIACION DE PROFESIONALES PARA EL DESARROLLO
    Sigla: AGRODASIN
    OBJETO SOCIAL PRINCIPAL: Desarrollo de proyectos agropecuarios y pesqueros
    ACTIVOS: $150,000,000
    PATRIMONIO: $80,000,000
    REPRESENTANTE LEGAL: CARLOS MARTINEZ
    Estado: ACTIVA
    """
    
    extractor = ExtractorCertificado()
    resultado = extractor.extraer(texto)
    
    assert resultado['nit'] == '8060130247'
    assert 'ASOCIACION' in resultado['razon_social']
    assert resultado['activos'] == 150000000.0
    assert resultado['patrimonio'] == 80000000.0
    assert resultado['estado'] == 'ACTIVO'


def test_extractor_rut():
    """Test RUT extractor"""
    texto = """
    REGISTRO UNICO TRIBUTARIO
    NIT: 8060130247
    RAZON SOCIAL: ASOCIACION DE PROFESIONALES
    ACTIVIDAD ECONOMICA: 0311 - PESCA MARITIMA
    Estado: ACTIVO
    """
    
    extractor = ExtractorRUT()
    resultado = extractor.extraer(texto)
    
    assert resultado['nit'] == '8060130247'
    assert 'ASOCIACION' in resultado['razon_social']
    assert 'PESCA' in resultado['actividad_economica']
    assert resultado['estado'] == 'ACTIVO'


def test_extractor_aviso():
    """Test tender notice extractor"""
    texto = """
    AVISO DE CONVOCATORIA
    PROCESO: LP-2024-001
    ENTIDAD: GOBERNACION DEL DEPARTAMENTO
    OBJETO DEL CONTRATO: Contratar la ejecución del proyecto para fortalecimiento
    de capacidades productivas de pesca artesanal
    VALOR ESTIMADO: $200,000,000
    PLAZO: 12 meses
    """
    
    extractor = ExtractorAviso()
    resultado = extractor.extraer(texto)
    
    assert resultado['numero_proceso'] == 'LP-2024-001'
    assert 'GOBERNACION' in resultado['entidad']
    assert 'pesca' in resultado['objeto_contrato'].lower()
    assert resultado['valor_estimado'] == 200000000.0
    assert 'meses' in resultado['plazo']


def test_extractor_certificado_missing_data():
    """Test certificate extractor with missing data"""
    texto = "Texto incompleto sin datos estructurados"
    
    extractor = ExtractorCertificado()
    resultado = extractor.extraer(texto)
    
    # Should not crash, should return None for missing fields
    assert resultado['nit'] is None
    assert resultado['razon_social'] is None
    assert resultado['activos'] is None
