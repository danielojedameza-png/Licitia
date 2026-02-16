"""Integration tests for combined analysis + pricing system"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoints():
    """Test all health check endpoints"""
    # Pricing health
    response = client.get("/api/pricing/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    
    # Analysis health
    response = client.get("/api/analysis/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["modules_loaded"] is True


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "LicitIA Hybrid Monetization API"
    assert "pricing" in data["endpoints"]


def test_analysis_demo_text():
    """Test analysis with text inputs"""
    response = client.post(
        "/api/analysis/demo",
        params={
            "certificado": "NIT: 123456789 Razón Social: TEST COMPANY OBJETO SOCIAL: Desarrollo de proyectos Estado: ACTIVA",
            "rut": "NIT: 123456789 Estado: ACTIVO ACTIVIDAD ECONOMICA: Construcción",
            "aviso": "PROCESO: LP-2024-001 OBJETO: Construcción de infraestructura VALOR: $100,000,000",
            "valor_proceso": 100000000
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "semaforo" in data
    assert "score" in data
    assert "similitud" in data
    assert "recomendacion" in data
    assert data["semaforo"] in ["VERDE", "AMARILLO", "ROJO"]


def test_subscription_plans():
    """Test subscription plans endpoint"""
    response = client.get("/api/pricing/subscription-plans")
    assert response.status_code == 200
    data = response.json()
    
    # The response is a dict with plan names as keys
    assert "POPULAR" in data
    assert "PYME" in data
    assert "EMPRESA" in data
    assert len(data) == 3
    
    # Check plan structure
    assert data["POPULAR"]["price"] == 19900
    assert data["PYME"]["price"] == 49900
    assert data["EMPRESA"]["price"] == 129900


def test_plus_pricing():
    """Test PLUS pricing calculation"""
    response = client.post(
        "/api/pricing/plus",
        json={
            "assets": 150000000,
            "process_value": 100000000
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "final_price" in data
    assert "base_price" in data
    assert data["final_price"] > 0


def test_pro_pricing():
    """Test PRO pricing calculation"""
    response = client.post(
        "/api/pricing/pro",
        json={
            "assets": 500000000,
            "process_value": 300000000,
            "num_annexes": 15
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "final_price" in data
    assert "annexes_surcharge" in data
    assert data["final_price"] > 0


def test_complete_quote():
    """Test complete quote endpoint"""
    response = client.post(
        "/api/pricing/quote",
        json={
            "assets": 200000000,
            "process_value": 150000000,
            "num_annexes": 10
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "plus" in data
    assert "pro" in data
    assert "subscription_plans" in data


def test_capped_pricing_mode():
    """Test capped pricing mode (20-80K)"""
    response = client.post(
        "/api/pricing/plus",
        json={
            "assets": 1000000000,
            "process_value": 500000000,
            "pricing_mode": "capped"
        }
    )
    assert response.status_code == 200
    data = response.json()
    # In capped mode, price should not exceed 80000
    assert data["final_price"] <= 80000
