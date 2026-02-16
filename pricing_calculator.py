"""
Pricing Calculator for LicitIA Hybrid Monetization Model
Implements all pricing calculation logic for PLUS and PRO tiers
"""

from typing import Optional, Dict, Any
from pricing_config import (
    AssetBand,
    ProcessValueBand,
    UserType,
    ASSET_BAND_THRESHOLDS,
    PROCESS_VALUE_BAND_THRESHOLDS,
    PLUS_MINIMUM_BY_ASSETS,
    PLUS_PERCENTAGE_BY_VALUE,
    PRO_MINIMUM_BY_ASSETS,
    PRO_PERCENTAGE_BY_VALUE,
    PRO_ANNEXES,
    PRO_CEILING,
    SOCIAL_DISCOUNT,
    SUBSCRIPTION_PLANS,
    PACKAGE_DISCOUNTS
)


def _round_currency(value: float) -> int:
    """
    Round currency value to nearest integer.
    Uses round() instead of int() to handle floating point precision issues.
    
    Args:
        value: Float value to round
        
    Returns:
        Rounded integer value
    """
    return int(round(value))


def get_asset_band(assets: int) -> AssetBand:
    """
    Determine the asset band based on asset value.
    
    Args:
        assets: Asset value in COP (0 if not informed)
        
    Returns:
        AssetBand enum value
    """
    if assets == 0:
        return AssetBand.A0
    
    for band, (min_val, max_val) in ASSET_BAND_THRESHOLDS.items():
        if min_val <= assets < max_val:
            return band
    
    return AssetBand.A3  # Default to highest if exceeds all


def get_process_value_band(process_value: int) -> ProcessValueBand:
    """
    Determine the process value band based on process value.
    
    Args:
        process_value: Process value in COP
        
    Returns:
        ProcessValueBand enum value
    """
    for band, (min_val, max_val) in PROCESS_VALUE_BAND_THRESHOLDS.items():
        if min_val <= process_value < max_val:
            return band
    
    return ProcessValueBand.V5  # Default to highest if exceeds all


def calculate_plus_price(
    assets: int,
    process_value: int,
    user_type: UserType = UserType.REGULAR
) -> Dict[str, Any]:
    """
    Calculate PLUS tier pricing (quick validation).
    
    Formula: Price = MAX(MinimumByAssets, PercentageOfProcessValue)
    
    Args:
        assets: Asset value in COP (0 if not informed)
        process_value: Process value in COP
        user_type: Type of user for discount eligibility
        
    Returns:
        Dictionary with pricing breakdown
    """
    asset_band = get_asset_band(assets)
    process_band = get_process_value_band(process_value)
    
    # Get minimum by assets
    minimum_by_assets = PLUS_MINIMUM_BY_ASSETS[asset_band]
    
    # Calculate percentage-based price
    percentage_config = PLUS_PERCENTAGE_BY_VALUE[process_band]
    percentage_price = _round_currency(process_value * percentage_config["percentage"])
    
    # Apply V1 minimum if specified
    if percentage_config["minimum"] is not None:
        percentage_price = max(percentage_price, percentage_config["minimum"])
    
    # Get the maximum between both
    base_price = max(minimum_by_assets, percentage_price)
    
    # Check for social discount
    discount_amount = 0
    final_price = base_price
    
    if is_eligible_for_social_discount(user_type, asset_band, process_band):
        discount_amount = _round_currency(base_price * SOCIAL_DISCOUNT["percentage"])
        final_price = base_price - discount_amount
    
    return {
        "service": "PLUS",
        "asset_band": asset_band.value,
        "process_band": process_band.value,
        "minimum_by_assets": minimum_by_assets,
        "percentage_based_price": percentage_price,
        "base_price": base_price,
        "discount_applied": discount_amount > 0,
        "discount_amount": discount_amount,
        "final_price": final_price,
        "breakdown": {
            "assets": assets,
            "process_value": process_value,
            "user_type": user_type.value
        }
    }


def calculate_pro_price(
    assets: int,
    process_value: int,
    num_annexes: int = 0,
    user_type: UserType = UserType.REGULAR
) -> Dict[str, Any]:
    """
    Calculate PRO tier pricing (complete analysis).
    
    Formula: Price = MAX(MinimumByAssets, PercentageOfProcessValue) + AnnexesSurcharge
    Ceiling: $1,490,000
    
    Args:
        assets: Asset value in COP (0 if not informed)
        process_value: Process value in COP
        num_annexes: Number of annex files (first 10 included)
        user_type: Type of user for discount eligibility
        
    Returns:
        Dictionary with pricing breakdown
    """
    asset_band = get_asset_band(assets)
    process_band = get_process_value_band(process_value)
    
    # Get minimum by assets
    minimum_by_assets = PRO_MINIMUM_BY_ASSETS[asset_band]
    
    # Calculate percentage-based price
    percentage = PRO_PERCENTAGE_BY_VALUE[process_band]
    percentage_price = _round_currency(process_value * percentage)
    
    # Get the maximum between both
    base_price = max(minimum_by_assets, percentage_price)
    
    # Calculate annexes surcharge
    annexes_surcharge = 0
    if num_annexes > PRO_ANNEXES["included"]:
        extra_annexes = num_annexes - PRO_ANNEXES["included"]
        
        # Check if package is better deal
        num_packages = extra_annexes // PRO_ANNEXES["package_10_count"]
        remaining = extra_annexes % PRO_ANNEXES["package_10_count"]
        
        package_price = (num_packages * PRO_ANNEXES["package_10_price"] + 
                        remaining * PRO_ANNEXES["additional_price"])
        individual_price = extra_annexes * PRO_ANNEXES["additional_price"]
        
        annexes_surcharge = min(package_price, individual_price)
    
    # Total before ceiling and discount
    price_before_discount = base_price + annexes_surcharge
    
    # Apply ceiling
    price_before_discount = min(price_before_discount, PRO_CEILING)
    
    # Check for social discount
    discount_amount = 0
    final_price = price_before_discount
    
    if is_eligible_for_social_discount(user_type, asset_band, process_band):
        discount_amount = _round_currency(price_before_discount * SOCIAL_DISCOUNT["percentage"])
        final_price = price_before_discount - discount_amount
    
    # Check if ceiling was exceeded
    ceiling_exceeded = (base_price + annexes_surcharge) > PRO_CEILING
    
    return {
        "service": "PRO",
        "asset_band": asset_band.value,
        "process_band": process_band.value,
        "minimum_by_assets": minimum_by_assets,
        "percentage_based_price": percentage_price,
        "base_price": base_price,
        "annexes_surcharge": annexes_surcharge,
        "num_annexes": num_annexes,
        "included_annexes": PRO_ANNEXES["included"],
        "price_before_discount": price_before_discount,
        "discount_applied": discount_amount > 0,
        "discount_amount": discount_amount,
        "final_price": final_price,
        "ceiling_exceeded": ceiling_exceeded,
        "ceiling_value": PRO_CEILING if ceiling_exceeded else None,
        "breakdown": {
            "assets": assets,
            "process_value": process_value,
            "user_type": user_type.value
        }
    }


def is_eligible_for_social_discount(
    user_type: UserType,
    asset_band: AssetBand,
    process_band: ProcessValueBand
) -> bool:
    """
    Check if user is eligible for 30% social discount.
    
    Criteria (ALL must be met):
    1. User type is productor/economia_popular/asociacion
    2. Assets: A0 or A1 (≤ $200M)
    3. Process value: V1 or V2 (≤ $200M)
    
    Args:
        user_type: Type of user
        asset_band: Asset band
        process_band: Process value band
        
    Returns:
        True if eligible for discount
    """
    # Check user type
    if user_type not in SOCIAL_DISCOUNT["eligible_user_types"]:
        return False
    
    # Check asset band
    if asset_band not in [AssetBand.A0, SOCIAL_DISCOUNT["max_assets_band"]]:
        return False
    
    # Check process value band
    if process_band not in SOCIAL_DISCOUNT["max_process_bands"]:
        return False
    
    return True


def calculate_package_discount(
    base_price: int,
    quantity: int,
    service: str = "PRO"
) -> Dict[str, Any]:
    """
    Calculate package discount for multiple processes.
    
    Args:
        base_price: Price per process
        quantity: Number of processes
        service: Service type (PRO only for packages)
        
    Returns:
        Dictionary with package pricing
    """
    if service != "PRO":
        return {
            "error": "Package discounts only available for PRO service",
            "total": base_price * quantity
        }
    
    total_without_discount = base_price * quantity
    discount_percentage = 0
    
    # Check if quantity qualifies for package discount
    if quantity >= PACKAGE_DISCOUNTS["pro_5_pack"]["quantity"]:
        discount_percentage = PACKAGE_DISCOUNTS["pro_5_pack"]["discount"]
    elif quantity >= PACKAGE_DISCOUNTS["pro_3_pack"]["quantity"]:
        discount_percentage = PACKAGE_DISCOUNTS["pro_3_pack"]["discount"]
    
    discount_amount = _round_currency(total_without_discount * discount_percentage)
    final_total = total_without_discount - discount_amount
    
    return {
        "service": service,
        "quantity": quantity,
        "price_per_process": base_price,
        "total_without_discount": total_without_discount,
        "discount_percentage": discount_percentage,
        "discount_amount": discount_amount,
        "final_total": final_total,
        "price_per_process_after_discount": final_total // quantity if quantity > 0 else 0
    }


def get_subscription_plans() -> Dict[str, Any]:
    """
    Get all available subscription plans.
    
    Returns:
        Dictionary with all subscription plans
    """
    return SUBSCRIPTION_PLANS


def calculate_complete_quote(
    assets: int,
    process_value: int,
    num_annexes: int = 0,
    user_type: UserType = UserType.REGULAR,
    include_subscription: bool = True
) -> Dict[str, Any]:
    """
    Calculate complete quote with PLUS, PRO, and subscription options.
    
    Args:
        assets: Asset value in COP
        process_value: Process value in COP
        num_annexes: Number of annex files
        user_type: Type of user
        include_subscription: Whether to include subscription plans
        
    Returns:
        Complete quote with all options
    """
    plus_pricing = calculate_plus_price(assets, process_value, user_type)
    pro_pricing = calculate_pro_price(assets, process_value, num_annexes, user_type)
    
    result = {
        "plus": plus_pricing,
        "pro": pro_pricing,
        "recommendation": "PRO" if num_annexes > 0 or process_value > 200_000_000 else "PLUS"
    }
    
    if include_subscription:
        result["subscription_plans"] = get_subscription_plans()
    
    return result
