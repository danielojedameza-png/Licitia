"""
Router for PRO file/document processing endpoints
"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/pro/archivos", tags=["pro_archivos"])


# Check if analysis modules are available
try:
    from ..demo_engine import DemoEngine, generar_mensaje_whatsapp
    from ..utils.pdf_handler import ManejadorDocumentos
    ANALYSIS_AVAILABLE = True
except ImportError:
    ANALYSIS_AVAILABLE = False
    logger.warning("Analysis modules not available")


if ANALYSIS_AVAILABLE:
    @router.post("/analyze")
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
    
    
    @router.post("/process-complete")
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
                from ..pricing_calculator import calculate_complete_quote
                from ..pricing_config import UserType
                
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


@router.get("/health")
async def health_check():
    """Health check endpoint for pro archivos"""
    return {
        "status": "ok",
        "service": "LicitIA PRO Archivos API",
        "analysis_available": ANALYSIS_AVAILABLE
    }
