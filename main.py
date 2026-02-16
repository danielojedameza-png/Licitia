from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any

from models import (
    PricingRequest,
    PackagePricingRequest,
    PlusPricingResponse,
    ProPricingResponse,
    PackagePricingResponse,
    CompleteQuoteResponse,
    ErrorResponse
)
from pricing_calculator import (
    calculate_plus_price,
    calculate_pro_price,
    calculate_package_discount,
    get_subscription_plans,
    calculate_complete_quote
)
from pricing_config import UserType

app = FastAPI(
    title="LicitIA - Hybrid Monetization API",
    description="API for calculating pricing for LicitIA's 3-pillar monetization model",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# Routers
pricing_router = APIRouter(prefix="/api/pricing", tags=["pricing"])
legacy_router = APIRouter(tags=["legacy"])


# ==================== PRICING ENDPOINTS ====================

@pricing_router.post("/plus", response_model=PlusPricingResponse)
async def calculate_plus(request: PricingRequest):
    """
    Calculate PLUS tier pricing (quick validation).
    
    PLUS includes:
    - Chamber validation
    - RUT validation
    - Quick fit assessment
    
    Formula: MAX(MinimumByAssets, PercentageOfProcessValue)
    """
    try:
        user_type = UserType[request.user_type.value.upper()] if request.user_type else UserType.REGULAR
        result = calculate_plus_price(
            assets=request.assets,
            process_value=request.process_value,
            user_type=user_type
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@pricing_router.post("/pro", response_model=ProPricingResponse)
async def calculate_pro(request: PricingRequest):
    """
    Calculate PRO tier pricing (complete analysis).
    
    PRO includes:
    - Deep analysis of pliegos and annexes
    - Strategic recommendations
    - Document review
    
    Formula: MAX(MinimumByAssets, PercentageOfProcessValue) + AnnexesSurcharge
    Ceiling: $1,490,000
    """
    try:
        user_type = UserType[request.user_type.value.upper()] if request.user_type else UserType.REGULAR
        result = calculate_pro_price(
            assets=request.assets,
            process_value=request.process_value,
            num_annexes=request.num_annexes,
            user_type=user_type
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@pricing_router.post("/package", response_model=PackagePricingResponse)
async def calculate_package(request: PackagePricingRequest):
    """
    Calculate package pricing for multiple processes.
    
    Discounts:
    - 3 processes: 15% discount
    - 5+ processes: 25% discount
    
    Only available for PRO service.
    """
    try:
        result = calculate_package_discount(
            base_price=request.base_price,
            quantity=request.quantity,
            service=request.service.value
        )
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@pricing_router.get("/subscription-plans")
async def get_subscription_plans_endpoint():
    """
    Get all available monthly subscription plans.
    
    Plans:
    - POPULAR: $19,900/month - 30 messages
    - PYME: $49,900/month - 120 messages
    - EMPRESA: $129,900/month - 400 messages
    """
    return get_subscription_plans()


@pricing_router.post("/quote", response_model=CompleteQuoteResponse)
async def get_complete_quote(
    request: PricingRequest,
    include_subscription: bool = True
):
    """
    Get complete pricing quote with PLUS, PRO, and subscription options.
    
    Returns all available pricing options with recommendations.
    """
    try:
        user_type = UserType[request.user_type.value.upper()] if request.user_type else UserType.REGULAR
        result = calculate_complete_quote(
            assets=request.assets,
            process_value=request.process_value,
            num_annexes=request.num_annexes,
            user_type=user_type,
            include_subscription=include_subscription
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@pricing_router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "LicitIA Pricing API"}


# ==================== LEGACY ENDPOINTS ====================

class Veredicto:
    def __init__(self, score):
        self.score = score


@legacy_router.get('/proplusplus_veredicto')
async def proplusplus_veredicto(value: int):
    """Legacy endpoint for score calculation"""
    score = await calcular_score(value)
    return {'score': score}


async def calcular_score(value):
    """Legacy score calculation"""
    return value * 2


# ==================== ROUTER REGISTRATION ====================

app.include_router(pricing_router)
app.include_router(legacy_router)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "service": "LicitIA Hybrid Monetization API",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "pricing": "/api/pricing",
            "health": "/api/pricing/health"
        }
    }