"""
Tests for capped pricing mode (20-80K model compatibility)
"""

import pytest
from pricing_calculator import (
    calculate_plus_price,
    calculate_pro_price,
    calculate_complete_quote
)
from pricing_config import UserType, PRICING_MODE_CAPPED, PRICING_MODE_ENTERPRISE, CAPPED_CEILING


class TestCappedPricingMode:
    """Tests for capped pricing mode (20-80K constrained model)"""
    
    def test_plus_capped_mode_applies_ceiling(self):
        """Test that capped mode applies $80K ceiling to PLUS pricing"""
        # This would normally be $250,000 in enterprise mode
        result = calculate_plus_price(
            assets=1_000_000_000,  # A3
            process_value=500_000_000,  # V3 -> 0.05% = $250,000
            pricing_mode=PRICING_MODE_CAPPED
        )
        
        assert result["pricing_mode"] == "capped"
        assert result["is_capped"] is True
        assert result["final_price"] == 80_000  # Capped at 80K
        assert result["final_price"] < result["percentage_based_price"]  # Was capped
    
    def test_plus_enterprise_mode_no_ceiling(self):
        """Test that enterprise mode does NOT cap PLUS pricing"""
        result = calculate_plus_price(
            assets=1_000_000_000,  # A3
            process_value=500_000_000,  # V3 -> 0.05% = $250,000
            pricing_mode=PRICING_MODE_ENTERPRISE
        )
        
        assert result["pricing_mode"] == "enterprise"
        assert result["is_capped"] is False
        assert result["final_price"] == 250_000  # NOT capped
    
    def test_plus_capped_mode_small_process_not_affected(self):
        """Test that small prices are not affected by capped mode"""
        result_capped = calculate_plus_price(
            assets=100_000_000,  # A1
            process_value=30_000_000,  # V1
            pricing_mode=PRICING_MODE_CAPPED
        )
        
        result_enterprise = calculate_plus_price(
            assets=100_000_000,  # A1
            process_value=30_000_000,  # V1
            pricing_mode=PRICING_MODE_ENTERPRISE
        )
        
        # Small prices should be the same in both modes
        assert result_capped["final_price"] == result_enterprise["final_price"]
        assert result_capped["final_price"] < 80_000
    
    def test_pro_capped_mode_applies_ceiling(self):
        """Test that capped mode applies $80K ceiling to PRO pricing"""
        # This would normally be $324,500 in enterprise mode
        result = calculate_pro_price(
            assets=500_000_000,  # A2
            process_value=300_000_000,  # V3
            num_annexes=15,
            pricing_mode=PRICING_MODE_CAPPED
        )
        
        assert result["pricing_mode"] == "capped"
        assert result["is_capped"] is True
        assert result["final_price"] == 80_000  # Capped at 80K
        assert result["ceiling_exceeded"] is True
    
    def test_pro_enterprise_mode_higher_ceiling(self):
        """Test that enterprise mode uses $1.49M ceiling for PRO"""
        result = calculate_pro_price(
            assets=500_000_000,  # A2
            process_value=300_000_000,  # V3
            num_annexes=15,
            pricing_mode=PRICING_MODE_ENTERPRISE
        )
        
        assert result["pricing_mode"] == "enterprise"
        assert result["is_capped"] is False
        assert result["final_price"] == 324_500  # NOT capped
        assert result["ceiling_exceeded"] is False
    
    def test_capped_mode_with_social_discount(self):
        """Test that social discount applies after capping"""
        # Use a scenario where social discount DOES apply (V1 or V2 with ≤200M)
        result = calculate_plus_price(
            assets=100_000_000,  # A1
            process_value=100_000_000,  # V2 (≤200M) -> eligible for discount
            user_type=UserType.PRODUCTOR,
            pricing_mode=PRICING_MODE_CAPPED
        )
        
        # Check eligibility first
        assert result["pricing_mode"] == "capped"
        assert result["discount_applied"] is True
        # 0.06% of 100M = 60K, max with A1 min (29,900) = 60K
        # With 30% discount: 60K - 18K = 42K
        assert result["base_price"] == 60_000
        assert result["discount_amount"] == 18_000  # 30% of 60K
        assert result["final_price"] == 42_000  # 60K - 18K
    
    def test_complete_quote_capped_mode(self):
        """Test complete quote in capped mode"""
        result = calculate_complete_quote(
            assets=500_000_000,
            process_value=300_000_000,
            num_annexes=10,
            pricing_mode=PRICING_MODE_CAPPED,
            include_subscription=False
        )
        
        assert result["pricing_mode"] == "capped"
        assert result["plus"]["is_capped"] is True
        assert result["pro"]["is_capped"] is True
        assert result["plus"]["final_price"] <= 80_000
        assert result["pro"]["final_price"] <= 80_000
    
    def test_capped_ceiling_constant(self):
        """Test that CAPPED_CEILING is correctly defined"""
        assert CAPPED_CEILING == 80_000
    
    def test_all_prices_in_range_for_capped_mode(self):
        """Test various scenarios to ensure all stay within 20-80K in capped mode"""
        test_cases = [
            (0, 10_000_000),  # A0 + V1
            (100_000_000, 50_000_000),  # A1 + V2
            (300_000_000, 100_000_000),  # A2 + V2
            (500_000_000, 300_000_000),  # A2 + V3
            (1_500_000_000, 500_000_000),  # A3 + V3
            (2_000_000_000, 3_000_000_000),  # A3 + V5
        ]
        
        for assets, process_value in test_cases:
            # Test PLUS
            plus_result = calculate_plus_price(
                assets=assets,
                process_value=process_value,
                pricing_mode=PRICING_MODE_CAPPED
            )
            assert plus_result["final_price"] <= 80_000, \
                f"PLUS price {plus_result['final_price']} exceeds 80K for assets={assets}, process={process_value}"
            
            # Test PRO
            pro_result = calculate_pro_price(
                assets=assets,
                process_value=process_value,
                num_annexes=20,
                pricing_mode=PRICING_MODE_CAPPED
            )
            assert pro_result["final_price"] <= 80_000, \
                f"PRO price {pro_result['final_price']} exceeds 80K for assets={assets}, process={process_value}"


class TestDefaultPricingMode:
    """Tests to ensure backward compatibility with default mode"""
    
    def test_default_mode_is_enterprise(self):
        """Test that default pricing mode is enterprise (backward compatible)"""
        result = calculate_plus_price(
            assets=100_000_000,
            process_value=50_000_000
        )
        
        assert result["pricing_mode"] == "enterprise"
        assert result["is_capped"] is False
    
    def test_pro_default_mode_is_enterprise(self):
        """Test that PRO default mode is enterprise"""
        result = calculate_pro_price(
            assets=100_000_000,
            process_value=50_000_000
        )
        
        assert result["pricing_mode"] == "enterprise"
        assert result["is_capped"] is False
    
    def test_complete_quote_default_mode(self):
        """Test complete quote default mode"""
        result = calculate_complete_quote(
            assets=100_000_000,
            process_value=50_000_000,
            include_subscription=False
        )
        
        assert result["pricing_mode"] == "enterprise"


class TestPricingModeComparison:
    """Tests comparing capped vs enterprise mode"""
    
    def test_small_prices_same_in_both_modes(self):
        """Prices under 80K should be identical in both modes"""
        test_cases = [
            (0, 10_000_000),  # Very small
            (100_000_000, 30_000_000),  # Small
            (200_000_000, 50_000_000),  # Medium-small
        ]
        
        for assets, process_value in test_cases:
            capped_result = calculate_plus_price(
                assets=assets,
                process_value=process_value,
                pricing_mode=PRICING_MODE_CAPPED
            )
            
            enterprise_result = calculate_plus_price(
                assets=assets,
                process_value=process_value,
                pricing_mode=PRICING_MODE_ENTERPRISE
            )
            
            if enterprise_result["final_price"] < 80_000:
                assert capped_result["final_price"] == enterprise_result["final_price"], \
                    f"Prices differ when under 80K: capped={capped_result['final_price']}, enterprise={enterprise_result['final_price']}"
    
    def test_large_prices_differ_between_modes(self):
        """Large processes should have different prices in capped vs enterprise"""
        assets = 1_000_000_000  # A3
        process_value = 500_000_000  # V3
        
        capped_result = calculate_plus_price(
            assets=assets,
            process_value=process_value,
            pricing_mode=PRICING_MODE_CAPPED
        )
        
        enterprise_result = calculate_plus_price(
            assets=assets,
            process_value=process_value,
            pricing_mode=PRICING_MODE_ENTERPRISE
        )
        
        # Capped should be 80K, enterprise should be much higher
        assert capped_result["final_price"] == 80_000
        assert enterprise_result["final_price"] > 80_000
        assert enterprise_result["final_price"] > capped_result["final_price"]
    
    def test_pro_ceiling_differs_by_mode(self):
        """PRO ceiling should be different in capped vs enterprise"""
        # Scenario that hits ceiling in both modes
        assets = 5_000_000_000
        process_value = 5_000_000_000
        
        capped_result = calculate_pro_price(
            assets=assets,
            process_value=process_value,
            num_annexes=0,
            pricing_mode=PRICING_MODE_CAPPED
        )
        
        enterprise_result = calculate_pro_price(
            assets=assets,
            process_value=process_value,
            num_annexes=0,
            pricing_mode=PRICING_MODE_ENTERPRISE
        )
        
        # Both should hit their respective ceilings
        assert capped_result["ceiling_exceeded"] is True
        assert capped_result["final_price"] == 80_000
        assert capped_result["ceiling_value"] == 80_000
        
        assert enterprise_result["ceiling_exceeded"] is True
        assert enterprise_result["final_price"] == 1_490_000
        assert enterprise_result["ceiling_value"] == 1_490_000
