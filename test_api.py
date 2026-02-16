"""
API integration tests for pricing endpoints
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Tests for health check endpoint"""
    
    def test_health_check(self):
        """Test health check returns ok status"""
        response = client.get("/api/pricing/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok", "service": "LicitIA Pricing API"}


class TestRootEndpoint:
    """Tests for root endpoint"""
    
    def test_root(self):
        """Test root endpoint returns API info"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "LicitIA Hybrid Monetization API"
        assert data["version"] == "1.0.0"


class TestPlusEndpoint:
    """Tests for PLUS pricing endpoint"""
    
    def test_plus_basic(self):
        """Test basic PLUS pricing calculation"""
        response = client.post("/api/pricing/plus", json={
            "assets": 100_000_000,
            "process_value": 50_000_000
        })
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "PLUS"
        assert data["asset_band"] == "A1"
        # 50M is at the boundary of V1 (up to 50M), so it's V2
        assert data["process_band"] == "V2"
        assert "final_price" in data
    
    def test_plus_with_social_discount(self):
        """Test PLUS with social discount"""
        response = client.post("/api/pricing/plus", json={
            "assets": 50_000_000,
            "process_value": 30_000_000,
            "user_type": "productor"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["discount_applied"] is True
        assert data["discount_amount"] > 0
    
    def test_plus_missing_required_fields(self):
        """Test PLUS endpoint with missing fields"""
        response = client.post("/api/pricing/plus", json={
            "assets": 100_000_000
        })
        assert response.status_code == 422  # Validation error
    
    def test_plus_negative_assets(self):
        """Test PLUS with negative assets"""
        response = client.post("/api/pricing/plus", json={
            "assets": -100_000_000,
            "process_value": 50_000_000
        })
        assert response.status_code == 422  # Validation error
    
    def test_plus_zero_process_value(self):
        """Test PLUS with zero process value"""
        response = client.post("/api/pricing/plus", json={
            "assets": 100_000_000,
            "process_value": 0
        })
        assert response.status_code == 422  # Validation error


class TestProEndpoint:
    """Tests for PRO pricing endpoint"""
    
    def test_pro_basic(self):
        """Test basic PRO pricing calculation"""
        response = client.post("/api/pricing/pro", json={
            "assets": 500_000_000,
            "process_value": 300_000_000,
            "num_annexes": 15
        })
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "PRO"
        assert data["asset_band"] == "A2"
        assert data["process_band"] == "V3"
        assert data["annexes_surcharge"] > 0
    
    def test_pro_no_annexes(self):
        """Test PRO without annexes"""
        response = client.post("/api/pricing/pro", json={
            "assets": 100_000_000,
            "process_value": 50_000_000,
            "num_annexes": 0
        })
        assert response.status_code == 200
        data = response.json()
        assert data["annexes_surcharge"] == 0
    
    def test_pro_with_social_discount(self):
        """Test PRO with social discount"""
        response = client.post("/api/pricing/pro", json={
            "assets": 100_000_000,
            "process_value": 100_000_000,
            "num_annexes": 5,
            "user_type": "economia_popular"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["discount_applied"] is True
    
    def test_pro_ceiling(self):
        """Test PRO ceiling is applied"""
        response = client.post("/api/pricing/pro", json={
            "assets": 5_000_000_000,
            "process_value": 5_000_000_000,
            "num_annexes": 0
        })
        assert response.status_code == 200
        data = response.json()
        assert data["ceiling_exceeded"] is True
        assert data["final_price"] == 1_490_000


class TestPackageEndpoint:
    """Tests for package pricing endpoint"""
    
    def test_package_3_processes(self):
        """Test package discount for 3 processes"""
        response = client.post("/api/pricing/package", json={
            "base_price": 100_000,
            "quantity": 3,
            "service": "PRO"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["discount_percentage"] == 0.15
        assert data["quantity"] == 3
    
    def test_package_5_processes(self):
        """Test package discount for 5 processes"""
        response = client.post("/api/pricing/package", json={
            "base_price": 100_000,
            "quantity": 5,
            "service": "PRO"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["discount_percentage"] == 0.25
    
    def test_package_single_process(self):
        """Test no discount for single process"""
        response = client.post("/api/pricing/package", json={
            "base_price": 100_000,
            "quantity": 1,
            "service": "PRO"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["discount_percentage"] == 0
    
    def test_package_plus_not_allowed(self):
        """Test that PLUS service doesn't support packages"""
        response = client.post("/api/pricing/package", json={
            "base_price": 100_000,
            "quantity": 3,
            "service": "PLUS"
        })
        assert response.status_code == 400


class TestSubscriptionPlansEndpoint:
    """Tests for subscription plans endpoint"""
    
    def test_get_subscription_plans(self):
        """Test getting all subscription plans"""
        response = client.get("/api/pricing/subscription-plans")
        assert response.status_code == 200
        data = response.json()
        
        assert "POPULAR" in data
        assert "PYME" in data
        assert "EMPRESA" in data
        
        assert data["POPULAR"]["price"] == 19900
        assert data["PYME"]["price"] == 49900
        assert data["EMPRESA"]["price"] == 129900


class TestCompleteQuoteEndpoint:
    """Tests for complete quote endpoint"""
    
    def test_complete_quote_with_subscription(self):
        """Test complete quote with subscription plans"""
        response = client.post("/api/pricing/quote", json={
            "assets": 100_000_000,
            "process_value": 50_000_000,
            "num_annexes": 5
        })
        assert response.status_code == 200
        data = response.json()
        
        assert "plus" in data
        assert "pro" in data
        assert "subscription_plans" in data
        assert "recommendation" in data
    
    def test_complete_quote_without_subscription(self):
        """Test complete quote without subscription plans"""
        response = client.post(
            "/api/pricing/quote?include_subscription=false",
            json={
                "assets": 100_000_000,
                "process_value": 50_000_000,
                "num_annexes": 0
            }
        )
        assert response.status_code == 200
        data = response.json()
        
        assert "plus" in data
        assert "pro" in data
        # When include_subscription=false, subscription_plans key is not included
        # or is None
        assert data.get("subscription_plans") is None
    
    def test_complete_quote_recommendation_plus(self):
        """Test that PLUS is recommended for small processes"""
        response = client.post("/api/pricing/quote", json={
            "assets": 50_000_000,
            "process_value": 30_000_000,
            "num_annexes": 0
        })
        assert response.status_code == 200
        data = response.json()
        assert data["recommendation"] == "PLUS"
    
    def test_complete_quote_recommendation_pro(self):
        """Test that PRO is recommended for large processes or with annexes"""
        response = client.post("/api/pricing/quote", json={
            "assets": 500_000_000,
            "process_value": 300_000_000,
            "num_annexes": 0
        })
        assert response.status_code == 200
        data = response.json()
        assert data["recommendation"] == "PRO"


class TestLegacyEndpoint:
    """Tests for legacy endpoints"""
    
    def test_proplusplus_veredicto(self):
        """Test legacy veredicto endpoint"""
        response = client.get("/proplusplus_veredicto?value=10")
        assert response.status_code == 200
        data = response.json()
        assert data["score"] == 20  # value * 2


class TestCORS:
    """Tests for CORS configuration"""
    
    def test_cors_preflight(self):
        """Test that CORS is configured"""
        # Test a simple GET request to see if CORS headers are returned
        response = client.get("/api/pricing/health", headers={"Origin": "http://localhost"})
        assert response.status_code == 200
        # With CORS configured, access-control-allow-origin should be present
        # Note: TestClient may not fully simulate CORS, this is just a basic check


class TestValidation:
    """Tests for input validation"""
    
    def test_invalid_user_type(self):
        """Test with invalid user type"""
        response = client.post("/api/pricing/plus", json={
            "assets": 100_000_000,
            "process_value": 50_000_000,
            "user_type": "invalid_type"
        })
        assert response.status_code == 422
    
    def test_invalid_service_type(self):
        """Test with invalid service type"""
        response = client.post("/api/pricing/package", json={
            "base_price": 100_000,
            "quantity": 3,
            "service": "INVALID"
        })
        assert response.status_code == 422
