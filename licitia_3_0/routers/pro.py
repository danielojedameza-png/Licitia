"""
Router for PRO tier endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
from ..models import PricingRequest, ProPricingResponse, UserTypeEnum
from ..pricing_calculator import calculate_pro_price
from ..pricing_config import UserType


# Create router
router = APIRouter(prefix="/api/pro", tags=["pro"])


def _convert_user_type(user_type: Optional[UserTypeEnum]) -> UserType:
    """Convert Pydantic UserTypeEnum to pricing_config UserType."""
    if user_type is None:
        return UserType.REGULAR
    
    try:
        return UserType[user_type.value.upper()]
    except (KeyError, AttributeError):
        return UserType.REGULAR


@router.post("/calculate", response_model=ProPricingResponse)
async def calculate_pro(request: PricingRequest):
    """
    Calculate PRO tier pricing (complete analysis).
    
    PRO includes:
    - Deep analysis of pliegos and annexes
    - Strategic recommendations
    - Document review
    
    Formula: MAX(MinimumByAssets, PercentageOfProcessValue) + AnnexesSurcharge
    
    Ceilings:
    - enterprise mode: $1,490,000
    - capped mode: $80,000
    """
    try:
        user_type = _convert_user_type(request.user_type)
        pricing_mode = request.pricing_mode.value if request.pricing_mode else "enterprise"
        
        result = calculate_pro_price(
            assets=request.assets,
            process_value=request.process_value,
            num_annexes=request.num_annexes,
            user_type=user_type,
            pricing_mode=pricing_mode
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint for pro"""
    return {"status": "ok", "service": "LicitIA PRO API"}
