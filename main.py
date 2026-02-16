from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, Optional

from models import (
    PricingRequest,
    PackagePricingRequest,
    PlusPricingResponse,
    ProPricingResponse,
    PackagePricingResponse,
    CompleteQuoteResponse,
    ErrorResponse,
    UserTypeEnum
)
from pricing_calculator import (
    calculate_plus_price,
    calculate_pro_price,
    calculate_package_discount,
    get_subscription_plans,
    calculate_complete_quote
)
from pricing_config import UserType


def _convert_user_type(user_type: Optional[UserTypeEnum]) -> UserType:
    """
    Convert Pydantic UserTypeEnum to pricing_config UserType.
    
    Args:
        user_type: Optional UserTypeEnum from request
        
    Returns:
        UserType enum value
    """
    if user_type is None:
        return UserType.REGULAR
    
    try:
        return UserType[user_type.value.upper()]
    except (KeyError, AttributeError):
        return UserType.REGULAR

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
    
    Pricing Modes:
    - enterprise: Full range (default, no cap)
    - capped: 20-80K constrained model (max $80,000)
    """
    try:
        user_type = _convert_user_type(request.user_type)
        pricing_mode = request.pricing_mode.value if request.pricing_mode else "enterprise"
        
        result = calculate_plus_price(
            assets=request.assets,
            process_value=request.process_value,
            user_type=user_type,
            pricing_mode=pricing_mode
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
    
    Pricing Modes:
    - enterprise: Full range (default)
    - capped: 20-80K constrained model
    """
    try:
        user_type = _convert_user_type(request.user_type)
        pricing_mode = request.pricing_mode.value if request.pricing_mode else "enterprise"
        
        result = calculate_complete_quote(
            assets=request.assets,
            process_value=request.process_value,
            num_annexes=request.num_annexes,
            user_type=user_type,
            include_subscription=include_subscription,
            pricing_mode=pricing_mode
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

# ==================== ANALYSIS ENDPOINTS ====================

try:
    from demo_engine import DemoEngine, generar_mensaje_whatsapp
    from utils.pdf_handler import ManejadorDocumentos
    from fastapi import UploadFile, File
    ANALYSIS_AVAILABLE = True
except ImportError:
    ANALYSIS_AVAILABLE = False


if ANALYSIS_AVAILABLE:
    analysis_router = APIRouter(prefix="/api/analysis", tags=["analysis"])
    
    
    @analysis_router.post("/demo")
    async def analyze_demo_text(
        certificado: str,
        rut: str,
        aviso: str,
        valor_proceso: Optional[float] = None
    ):
        """
        DEMO analysis using text inputs.
        
        Args:
            certificado: Certificate text
            rut: RUT text
            aviso: Tender notice text
            valor_proceso: Optional process value
            
        Returns:
            Complete analysis with score, traffic light, and recommendations
        """
        try:
            engine = DemoEngine()
            resultado = engine.analizar(certificado, rut, aviso, valor_proceso)
            return resultado
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")
    
    
    @analysis_router.post("/demo-files")
    async def analyze_demo_files(
        certificado: UploadFile = File(...),
        rut: UploadFile = File(...),
        aviso: UploadFile = File(...),
        valor_proceso: Optional[float] = None
    ):
        """
        DEMO analysis using file uploads (PDF).
        
        Upload PDF files for automatic text extraction and analysis.
        
        Args:
            certificado: Certificate PDF file
            rut: RUT PDF file
            aviso: Tender notice PDF file
            valor_proceso: Optional process value
            
        Returns:
            Complete analysis with score, traffic light, and recommendations
        """
        try:
            manejador = ManejadorDocumentos()
            
            # Extract text from PDFs
            cert_bytes = await certificado.read()
            rut_bytes = await rut.read()
            aviso_bytes = await aviso.read()
            
            cert_result = manejador.procesar_pdf(cert_bytes, tipo='bytes')
            rut_result = manejador.procesar_pdf(rut_bytes, tipo='bytes')
            aviso_result = manejador.procesar_pdf(aviso_bytes, tipo='bytes')
            
            if not cert_result['exito']:
                raise HTTPException(status_code=400, detail=f"Certificate PDF error: {cert_result['error']}")
            if not rut_result['exito']:
                raise HTTPException(status_code=400, detail=f"RUT PDF error: {rut_result['error']}")
            if not aviso_result['exito']:
                raise HTTPException(status_code=400, detail=f"Notice PDF error: {aviso_result['error']}")
            
            # Analyze
            engine = DemoEngine()
            resultado = engine.analizar(
                cert_result['texto'],
                rut_result['texto'],
                aviso_result['texto'],
                valor_proceso
            )
            
            return resultado
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")
    
    
    @analysis_router.post("/process")
    async def process_complete(
        certificado: UploadFile = File(...),
        rut: UploadFile = File(...),
        aviso: UploadFile = File(...),
        valor_proceso: Optional[float] = None,
        include_pricing: bool = True,
        pricing_mode: str = "enterprise"
    ):
        """
        Complete process: Analysis + Pricing quote.
        
        Combines document analysis with automatic pricing calculation.
        
        Args:
            certificado: Certificate PDF file
            rut: RUT PDF file
            aviso: Tender notice PDF file
            valor_proceso: Optional process value
            include_pricing: Include pricing quote (default: True)
            pricing_mode: "enterprise" or "capped" (default: "enterprise")
            
        Returns:
            Analysis results + pricing quote
        """
        try:
            manejador = ManejadorDocumentos()
            
            # Extract text from PDFs
            cert_bytes = await certificado.read()
            rut_bytes = await rut.read()
            aviso_bytes = await aviso.read()
            
            cert_result = manejador.procesar_pdf(cert_bytes, tipo='bytes')
            rut_result = manejador.procesar_pdf(rut_bytes, tipo='bytes')
            aviso_result = manejador.procesar_pdf(aviso_bytes, tipo='bytes')
            
            if not cert_result['exito']:
                raise HTTPException(status_code=400, detail=f"Certificate PDF error: {cert_result['error']}")
            if not rut_result['exito']:
                raise HTTPException(status_code=400, detail=f"RUT PDF error: {rut_result['error']}")
            if not aviso_result['exito']:
                raise HTTPException(status_code=400, detail=f"Notice PDF error: {aviso_result['error']}")
            
            # Analyze
            engine = DemoEngine()
            resultado_analisis = engine.analizar(
                cert_result['texto'],
                rut_result['texto'],
                aviso_result['texto'],
                valor_proceso
            )
            
            # Add pricing if requested
            if include_pricing and valor_proceso:
                from pricing_calculator import calculate_complete_quote
                from pricing_config import UserType
                
                activos = resultado_analisis['datos_extraidos'].get('activos')
                
                if activos:
                    pricing_quote = calculate_complete_quote(
                        assets=activos,
                        process_value=valor_proceso,
                        num_annexes=10,  # Default
                        user_type=UserType.REGULAR,
                        include_subscription=True,
                        pricing_mode=pricing_mode
                    )
                    resultado_analisis['pricing'] = pricing_quote
            
            # Generate WhatsApp message
            resultado_analisis['whatsapp_message'] = generar_mensaje_whatsapp(resultado_analisis)
            
            return resultado_analisis
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
    
    
    @analysis_router.get("/health")
    async def analysis_health_check():
        """Health check for analysis system"""
        return {
            "status": "ok",
            "service": "LicitIA Analysis Engine",
            "modules_loaded": ANALYSIS_AVAILABLE
        }
    
    
    # Register analysis router
    app.include_router(analysis_router)
