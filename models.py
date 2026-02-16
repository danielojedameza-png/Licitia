"""
Pydantic models for pricing API requests and responses
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from enum import Enum


class PricingModeEnum(str, Enum):
    """Pricing mode for calculation"""
    capped = "capped"  # 20-80K constrained model
    enterprise = "enterprise"  # Full range model


class UserTypeEnum(str, Enum):
    """User type for social discount eligibility"""
    productor = "productor"
    economia_popular = "economia_popular"
    asociacion = "asociacion"
    regular = "regular"


class ServiceType(str, Enum):
    """Service type for pricing"""
    PLUS = "PLUS"
    PRO = "PRO"


class PricingRequest(BaseModel):
    """Request model for pricing calculation"""
    assets: int = Field(
        ...,
        ge=0,
        description="Asset value in COP (0 if not informed)"
    )
    process_value: int = Field(
        ...,
        gt=0,
        description="Process value in COP"
    )
    num_annexes: Optional[int] = Field(
        0,
        ge=0,
        description="Number of annex files (for PRO service)"
    )
    user_type: Optional[UserTypeEnum] = Field(
        UserTypeEnum.regular,
        description="User type for discount eligibility"
    )
    pricing_mode: Optional[PricingModeEnum] = Field(
        PricingModeEnum.enterprise,
        description="Pricing mode: 'capped' (20-80K max) or 'enterprise' (full range)"
    )

    @field_validator('assets')
    @classmethod
    def validate_assets(cls, v):
        if v < 0:
            raise ValueError('Assets cannot be negative')
        return v

    @field_validator('process_value')
    @classmethod
    def validate_process_value(cls, v):
        if v <= 0:
            raise ValueError('Process value must be greater than 0')
        return v


class PackagePricingRequest(BaseModel):
    """Request model for package pricing calculation"""
    base_price: int = Field(
        ...,
        gt=0,
        description="Price per individual process"
    )
    quantity: int = Field(
        ...,
        ge=1,
        description="Number of processes in package"
    )
    service: ServiceType = Field(
        ServiceType.PRO,
        description="Service type (PRO only for packages)"
    )


class BreakdownModel(BaseModel):
    """Pricing breakdown details"""
    assets: int
    process_value: int
    user_type: str


class PlusPricingResponse(BaseModel):
    """Response model for PLUS pricing"""
    service: str
    asset_band: str
    process_band: str
    minimum_by_assets: int
    percentage_based_price: int
    base_price: int
    discount_applied: bool
    discount_amount: int
    final_price: int
    pricing_mode: str
    is_capped: bool
    breakdown: BreakdownModel


class ProPricingResponse(BaseModel):
    """Response model for PRO pricing"""
    service: str
    asset_band: str
    process_band: str
    minimum_by_assets: int
    percentage_based_price: int
    base_price: int
    annexes_surcharge: int
    num_annexes: int
    included_annexes: int
    price_before_discount: int
    discount_applied: bool
    discount_amount: int
    final_price: int
    ceiling_exceeded: bool
    ceiling_value: Optional[int]
    pricing_mode: str
    is_capped: bool
    breakdown: BreakdownModel


class PackagePricingResponse(BaseModel):
    """Response model for package pricing"""
    service: str
    quantity: int
    price_per_process: int
    total_without_discount: int
    discount_percentage: float
    discount_amount: int
    final_total: int
    price_per_process_after_discount: int


class SubscriptionPlan(BaseModel):
    """Subscription plan details"""
    price: int
    messages: int
    features: List[str]


class SubscriptionPlansResponse(BaseModel):
    """Response model for subscription plans"""
    POPULAR: SubscriptionPlan
    PYME: SubscriptionPlan
    EMPRESA: SubscriptionPlan


class CompleteQuoteResponse(BaseModel):
    """Response model for complete quote"""
    plus: PlusPricingResponse
    pro: ProPricingResponse
    recommendation: str
    pricing_mode: str
    subscription_plans: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
