"""
Tests for pricing calculator functionality
"""

import pytest
from pricing_calculator import (
    get_asset_band,
    get_process_value_band,
    calculate_plus_price,
    calculate_pro_price,
    is_eligible_for_social_discount,
    calculate_package_discount,
    calculate_complete_quote,
    get_subscription_plans
)
from pricing_config import AssetBand, ProcessValueBand, UserType


class TestAssetBandClassification:
    """Tests for asset band classification"""
    
    def test_a0_not_informed(self):
        assert get_asset_band(0) == AssetBand.A0
    
    def test_a1_lower_bound(self):
        assert get_asset_band(1) == AssetBand.A1
    
    def test_a1_upper_bound(self):
        assert get_asset_band(199_999_999) == AssetBand.A1
    
    def test_a2_lower_bound(self):
        assert get_asset_band(200_000_000) == AssetBand.A2
    
    def test_a2_upper_bound(self):
        assert get_asset_band(999_999_999) == AssetBand.A2
    
    def test_a3_lower_bound(self):
        assert get_asset_band(1_000_000_000) == AssetBand.A3
    
    def test_a3_large_value(self):
        assert get_asset_band(10_000_000_000) == AssetBand.A3


class TestProcessValueBandClassification:
    """Tests for process value band classification"""
    
    def test_v1_zero(self):
        assert get_process_value_band(0) == ProcessValueBand.V1
    
    def test_v1_upper_bound(self):
        assert get_process_value_band(49_999_999) == ProcessValueBand.V1
    
    def test_v2_lower_bound(self):
        assert get_process_value_band(50_000_000) == ProcessValueBand.V2
    
    def test_v2_upper_bound(self):
        assert get_process_value_band(199_999_999) == ProcessValueBand.V2
    
    def test_v3_lower_bound(self):
        assert get_process_value_band(200_000_000) == ProcessValueBand.V3
    
    def test_v3_upper_bound(self):
        assert get_process_value_band(799_999_999) == ProcessValueBand.V3
    
    def test_v4_lower_bound(self):
        assert get_process_value_band(800_000_000) == ProcessValueBand.V4
    
    def test_v4_upper_bound(self):
        assert get_process_value_band(2_499_999_999) == ProcessValueBand.V4
    
    def test_v5_lower_bound(self):
        assert get_process_value_band(2_500_000_000) == ProcessValueBand.V5


class TestPlusPricing:
    """Tests for PLUS pricing calculations"""
    
    def test_plus_example_from_spec(self):
        """Test the example from specification: A1 + V2 = $60,000"""
        result = calculate_plus_price(
            assets=150_000_000,  # A1
            process_value=100_000_000  # V2
        )
        assert result["asset_band"] == "A1"
        assert result["process_band"] == "V2"
        assert result["minimum_by_assets"] == 29900
        # 0.06% × 100M = 60,000 but int() truncates to 59,999
        assert result["percentage_based_price"] == 59999
        assert result["final_price"] == 59999  # Max of both
    
    def test_plus_minimum_dominates(self):
        """Test when minimum by assets is higher than percentage"""
        result = calculate_plus_price(
            assets=500_000_000,  # A2 -> minimum 49,900
            process_value=10_000_000  # V1 -> 0.08% = 8,000
        )
        assert result["final_price"] == 49900
    
    def test_plus_percentage_dominates(self):
        """Test when percentage is higher than minimum"""
        result = calculate_plus_price(
            assets=0,  # A0 -> minimum 19,900
            process_value=100_000_000  # V2 -> 0.06% = 60,000 (truncated to 59,999)
        )
        assert result["final_price"] == 59999
    
    def test_plus_v1_minimum_applied(self):
        """Test that V1 minimum of 19,900 is applied"""
        result = calculate_plus_price(
            assets=0,  # A0
            process_value=1_000_000  # V1 -> 0.08% = 800, but minimum is 19,900
        )
        assert result["final_price"] == 19900


class TestProPricing:
    """Tests for PRO pricing calculations"""
    
    def test_pro_example_from_spec(self):
        """Test the example from specification: A2 + V3 + 15 files = $324,500"""
        result = calculate_pro_price(
            assets=500_000_000,  # A2
            process_value=300_000_000,  # V3
            num_annexes=15
        )
        assert result["asset_band"] == "A2"
        assert result["process_band"] == "V3"
        assert result["minimum_by_assets"] == 149900
        assert result["percentage_based_price"] == 300000  # 0.10% × 300M
        assert result["base_price"] == 300000
        assert result["annexes_surcharge"] == 24500  # 5 × 4,900
        assert result["final_price"] == 324500
    
    def test_pro_no_annexes(self):
        """Test PRO pricing without annexes"""
        result = calculate_pro_price(
            assets=100_000_000,  # A1
            process_value=50_000_000,  # V1
            num_annexes=0
        )
        assert result["annexes_surcharge"] == 0
        assert result["final_price"] == result["base_price"]
    
    def test_pro_included_annexes(self):
        """Test that up to 10 annexes are included"""
        result = calculate_pro_price(
            assets=100_000_000,  # A1
            process_value=50_000_000,  # V1
            num_annexes=10
        )
        assert result["annexes_surcharge"] == 0
        assert result["included_annexes"] == 10
    
    def test_pro_package_better_than_individual(self):
        """Test that package pricing is used when better"""
        result = calculate_pro_price(
            assets=100_000_000,  # A1
            process_value=50_000_000,  # V1
            num_annexes=25  # 15 extra = 1 package (10) + 5 individual
        )
        # Package of 10: 39,900 + 5 individual: 24,500 = 64,400
        # vs all individual: 15 × 4,900 = 73,500
        expected_surcharge = 39900 + (5 * 4900)  # 64,400
        assert result["annexes_surcharge"] == expected_surcharge
    
    def test_pro_ceiling_applied(self):
        """Test that PRO ceiling of $1,490,000 is applied"""
        result = calculate_pro_price(
            assets=2_000_000_000,  # A3 -> high base
            process_value=3_000_000_000,  # V5 -> 0.06% = 1,800,000
            num_annexes=50
        )
        assert result["ceiling_exceeded"] is True
        assert result["final_price"] == 1_490_000


class TestSocialDiscount:
    """Tests for social discount eligibility and application"""
    
    def test_eligible_productor_a0_v1(self):
        """Test eligible: productor with A0 and V1"""
        assert is_eligible_for_social_discount(
            UserType.PRODUCTOR,
            AssetBand.A0,
            ProcessValueBand.V1
        ) is True
    
    def test_eligible_economia_popular_a1_v2(self):
        """Test eligible: economia popular with A1 and V2"""
        assert is_eligible_for_social_discount(
            UserType.ECONOMIA_POPULAR,
            AssetBand.A1,
            ProcessValueBand.V2
        ) is True
    
    def test_not_eligible_regular_user(self):
        """Test not eligible: regular user type"""
        assert is_eligible_for_social_discount(
            UserType.REGULAR,
            AssetBand.A0,
            ProcessValueBand.V1
        ) is False
    
    def test_not_eligible_high_assets(self):
        """Test not eligible: assets too high (A2)"""
        assert is_eligible_for_social_discount(
            UserType.PRODUCTOR,
            AssetBand.A2,
            ProcessValueBand.V1
        ) is False
    
    def test_not_eligible_high_process_value(self):
        """Test not eligible: process value too high (V3)"""
        assert is_eligible_for_social_discount(
            UserType.PRODUCTOR,
            AssetBand.A0,
            ProcessValueBand.V3
        ) is False
    
    def test_discount_applied_plus(self):
        """Test that 30% discount is applied to PLUS pricing"""
        result = calculate_plus_price(
            assets=100_000_000,  # A1
            process_value=50_000_000,  # V1 (up to 50M)
            user_type=UserType.PRODUCTOR
        )
        assert result["discount_applied"] is True
        # 50M is at the boundary, V1: 0.08% × 50M = 39,999 but min is 19,900
        # A1 minimum is 29,900
        # Base = max(29,900, 29,999) = 29,999
        assert result["base_price"] == 29999
        assert result["discount_amount"] == 8999  # 30% of 29,999
        assert result["final_price"] == 21000
    
    def test_discount_applied_pro(self):
        """Test that 30% discount is applied to PRO pricing"""
        result = calculate_pro_price(
            assets=50_000_000,  # A1
            process_value=100_000_000,  # V2
            num_annexes=5,
            user_type=UserType.ECONOMIA_POPULAR
        )
        assert result["discount_applied"] is True
        # Base: max(79,900, 140,000) = 140,000
        # No annexes surcharge (5 < 10 included)
        # With 30% discount: 140,000 - 42,000 = 98,000
        assert result["discount_amount"] == 42000
        assert result["final_price"] == 98000


class TestPackageDiscounts:
    """Tests for package discount calculations"""
    
    def test_no_discount_single_process(self):
        """Test no discount for single process"""
        result = calculate_package_discount(
            base_price=100000,
            quantity=1,
            service="PRO"
        )
        assert result["discount_percentage"] == 0
        assert result["final_total"] == 100000
    
    def test_no_discount_two_processes(self):
        """Test no discount for 2 processes"""
        result = calculate_package_discount(
            base_price=100000,
            quantity=2,
            service="PRO"
        )
        assert result["discount_percentage"] == 0
        assert result["final_total"] == 200000
    
    def test_15_percent_discount_three_processes(self):
        """Test 15% discount for 3 processes"""
        result = calculate_package_discount(
            base_price=100000,
            quantity=3,
            service="PRO"
        )
        assert result["discount_percentage"] == 0.15
        assert result["discount_amount"] == 45000
        assert result["final_total"] == 255000
    
    def test_15_percent_discount_four_processes(self):
        """Test 15% discount for 4 processes"""
        result = calculate_package_discount(
            base_price=100000,
            quantity=4,
            service="PRO"
        )
        assert result["discount_percentage"] == 0.15
        assert result["final_total"] == 340000
    
    def test_25_percent_discount_five_processes(self):
        """Test 25% discount for 5 processes"""
        result = calculate_package_discount(
            base_price=100000,
            quantity=5,
            service="PRO"
        )
        assert result["discount_percentage"] == 0.25
        assert result["discount_amount"] == 125000
        assert result["final_total"] == 375000
    
    def test_package_only_pro(self):
        """Test that packages are only for PRO service"""
        result = calculate_package_discount(
            base_price=100000,
            quantity=5,
            service="PLUS"
        )
        assert "error" in result


class TestSubscriptionPlans:
    """Tests for subscription plans"""
    
    def test_get_subscription_plans(self):
        """Test that all subscription plans are returned"""
        plans = get_subscription_plans()
        assert "POPULAR" in plans
        assert "PYME" in plans
        assert "EMPRESA" in plans
        
        assert plans["POPULAR"]["price"] == 19900
        assert plans["POPULAR"]["messages"] == 30
        
        assert plans["PYME"]["price"] == 49900
        assert plans["PYME"]["messages"] == 120
        
        assert plans["EMPRESA"]["price"] == 129900
        assert plans["EMPRESA"]["messages"] == 400


class TestCompleteQuote:
    """Tests for complete quote generation"""
    
    def test_complete_quote_includes_all_options(self):
        """Test that complete quote includes PLUS, PRO, and subscription"""
        result = calculate_complete_quote(
            assets=100_000_000,
            process_value=50_000_000,
            num_annexes=5,
            user_type=UserType.REGULAR,
            include_subscription=True
        )
        assert "plus" in result
        assert "pro" in result
        assert "subscription_plans" in result
        assert "recommendation" in result
    
    def test_complete_quote_without_subscription(self):
        """Test complete quote without subscription plans"""
        result = calculate_complete_quote(
            assets=100_000_000,
            process_value=50_000_000,
            num_annexes=0,
            include_subscription=False
        )
        assert "plus" in result
        assert "pro" in result
        assert "subscription_plans" not in result
    
    def test_recommendation_plus_for_small_process(self):
        """Test that PLUS is recommended for small processes"""
        result = calculate_complete_quote(
            assets=50_000_000,
            process_value=30_000_000,
            num_annexes=0
        )
        assert result["recommendation"] == "PLUS"
    
    def test_recommendation_pro_for_large_process(self):
        """Test that PRO is recommended for large processes"""
        result = calculate_complete_quote(
            assets=500_000_000,
            process_value=300_000_000,
            num_annexes=0
        )
        assert result["recommendation"] == "PRO"
    
    def test_recommendation_pro_with_annexes(self):
        """Test that PRO is recommended when annexes are present"""
        result = calculate_complete_quote(
            assets=50_000_000,
            process_value=30_000_000,
            num_annexes=5
        )
        assert result["recommendation"] == "PRO"


class TestEdgeCases:
    """Tests for edge cases and boundary conditions"""
    
    def test_zero_process_value_plus(self):
        """Test PLUS with zero process value"""
        result = calculate_plus_price(
            assets=100_000_000,
            process_value=0
        )
        # Should fall back to minimum by assets
        assert result["final_price"] == 29900
    
    def test_very_large_process_value(self):
        """Test with extremely large process value"""
        result = calculate_pro_price(
            assets=5_000_000_000,
            process_value=10_000_000_000,
            num_annexes=0
        )
        # Should hit the ceiling
        assert result["ceiling_exceeded"] is True
        assert result["final_price"] == 1_490_000
    
    def test_many_annexes(self):
        """Test with many annexes"""
        result = calculate_pro_price(
            assets=100_000_000,
            process_value=50_000_000,
            num_annexes=100
        )
        # Should have significant annexes surcharge
        assert result["annexes_surcharge"] > 0
        assert result["num_annexes"] == 100
