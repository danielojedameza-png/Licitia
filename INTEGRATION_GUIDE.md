# LicitIA Integration Guide

## Overview

LicitIA is now a **complete tender analysis and pricing system** that combines:

1. **Document Analysis Engine** - Extracts and analyzes tender documents
2. **Pricing Calculator** - Calculates service pricing based on business rules
3. **REST API** - Provides easy access to all functionality

## System Architecture

```
LicitIA/
├── core/                    # Analysis engine
│   ├── extractor.py         # Document data extraction
│   ├── comparador.py        # Text similarity comparison
│   └── validador.py         # Document validation & scoring
├── utils/                   # Utilities
│   └── pdf_handler.py       # PDF text extraction
├── pricing_calculator.py    # Pricing business logic
├── pricing_config.py        # Pricing configuration
├── models.py                # Pydantic models
├── demo_engine.py           # Analysis orchestrator
└── main.py                  # FastAPI application
```

## Features

### 📄 Document Analysis
- **Certificate Extraction**: NIT, company name, business object, assets, legal status
- **RUT Extraction**: Tax ID, economic activity, status
- **Tender Notice Extraction**: Process number, entity, contract object, estimated value
- **Similarity Analysis**: Multi-algorithm text comparison with 50%+ accuracy
- **Validation**: Structural and financial capacity validation
- **Scoring**: 100-point scoring system with traffic light status (🟢🟡🔴)

### 💰 Pricing System
- **3-Pillar Model**: Subscription + Pay-per-Process + Premium
- **PLUS Service**: Quick validation ($19,900 - $79,900)
- **PRO Service**: Complete analysis ($49,900 - $1,490,000)
- **Social Discount**: -30% for eligible small businesses
- **Package Discounts**: 15% (3 processes) / 25% (5+ processes)
- **Dual Mode**: Enterprise (full range) / Capped (20-80K)

## API Endpoints

### Analysis Endpoints

#### 1. Text-Based Analysis
```bash
POST /api/analysis/demo
```
Analyze using plain text inputs (no file upload).

**Parameters:**
- `certificado`: Certificate text
- `rut`: RUT text
- `aviso`: Tender notice text
- `valor_proceso`: Process value (optional)

**Example:**
```bash
curl -X POST "http://localhost:8000/api/analysis/demo" \
  -d "certificado=NIT: 123456789..." \
  -d "rut=RUT text..." \
  -d "aviso=Tender notice..." \
  -d "valor_proceso=100000000"
```

#### 2. File-Based Analysis
```bash
POST /api/analysis/demo-files
```
Analyze using PDF file uploads.

**Form Data:**
- `certificado`: Certificate PDF file
- `rut`: RUT PDF file
- `aviso`: Tender notice PDF file
- `valor_proceso`: Process value (optional)

**Example:**
```bash
curl -X POST "http://localhost:8000/api/analysis/demo-files" \
  -F "certificado=@certificate.pdf" \
  -F "rut=@rut.pdf" \
  -F "aviso=@notice.pdf" \
  -F "valor_proceso=100000000"
```

**Response:**
```json
{
  "semaforo": "AMARILLO",
  "score": 65,
  "similitud": 0.45,
  "recomendacion": "Viable con ajustes. Score: 65/100...",
  "faltantes": ["RUP actualizado", "Pólizas requeridas"],
  "alertas": ["Activos por debajo del mínimo (74%)"],
  "score_detalle": {
    "score_total": 65,
    "score_estructura": 35,
    "score_encaje": 18,
    "score_financiero": 12
  },
  "datos_extraidos": {
    "nit": "123456789",
    "razon_social": "COMPANY NAME",
    "activos": 150000000,
    "valor_proceso": 100000000
  }
}
```

#### 3. Complete Process (Analysis + Pricing)
```bash
POST /api/analysis/process
```
Complete workflow: analyze documents and get pricing quote.

**Form Data:**
- `certificado`: Certificate PDF
- `rut`: RUT PDF
- `aviso`: Tender notice PDF
- `valor_proceso`: Process value (optional)
- `include_pricing`: Include pricing (default: true)
- `pricing_mode`: "enterprise" or "capped" (default: "enterprise")

**Response:** Analysis result + pricing quote + WhatsApp message

### Pricing Endpoints

#### 4. PLUS Pricing
```bash
POST /api/pricing/plus
```
Calculate PLUS service pricing.

**Body:**
```json
{
  "assets": 150000000,
  "process_value": 100000000,
  "user_type": "regular",
  "pricing_mode": "enterprise"
}
```

#### 5. PRO Pricing
```bash
POST /api/pricing/pro
```
Calculate PRO service pricing.

**Body:**
```json
{
  "assets": 500000000,
  "process_value": 300000000,
  "num_annexes": 15,
  "user_type": "regular",
  "pricing_mode": "enterprise"
}
```

#### 6. Complete Quote
```bash
POST /api/pricing/quote
```
Get PLUS, PRO, and subscription options together.

#### 7. Subscription Plans
```bash
GET /api/pricing/subscription-plans
```
Get all monthly subscription plans.

### Health Checks

```bash
GET /api/pricing/health
GET /api/analysis/health
```

## Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

**Required packages:**
- fastapi>=0.104.0
- pydantic>=2.0.0
- uvicorn>=0.24.0
- PyPDF2>=3.0.0
- python-multipart>=0.0.6
- pytest>=7.4.0
- httpx>=0.25.0

### 2. Run Server
```bash
uvicorn main:app --reload
```

Server will start at: http://localhost:8000

### 3. Access Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

### Run All Tests
```bash
pytest -v
```

**Test Coverage:**
- ✅ 98 tests total
- ✅ 87 pricing tests
- ✅ 4 analysis tests
- ✅ 8 integration tests
- ✅ 100% pass rate

### Run Specific Test Suites
```bash
# Pricing tests only
pytest test_pricing_calculator.py -v

# Analysis tests only
pytest tests/analysis/ -v

# Integration tests
pytest tests/test_integration.py -v
```

## Usage Examples

### Python Client Example
```python
import requests

# Analyze with text
response = requests.post(
    "http://localhost:8000/api/analysis/demo",
    params={
        "certificado": "NIT: 123456789...",
        "rut": "RUT data...",
        "aviso": "Tender notice...",
        "valor_proceso": 100000000
    }
)
result = response.json()
print(f"Score: {result['score']}/100")
print(f"Status: {result['semaforo']}")
print(f"Recommendation: {result['recomendacion']}")

# Get pricing quote
response = requests.post(
    "http://localhost:8000/api/pricing/quote",
    json={
        "assets": 150000000,
        "process_value": 100000000
    }
)
quote = response.json()
print(f"PLUS: ${quote['plus']['final_price']:,.0f}")
print(f"PRO: ${quote['pro']['final_price']:,.0f}")
```

### JavaScript Client Example
```javascript
// Analyze with file upload
const formData = new FormData();
formData.append('certificado', certificateFile);
formData.append('rut', rutFile);
formData.append('aviso', noticeFile);
formData.append('valor_proceso', 100000000);

const response = await fetch('http://localhost:8000/api/analysis/demo-files', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(`Score: ${result.score}/100`);
console.log(`Status: ${result.semaforo}`);
```

## Key Modules

### DemoEngine
Main orchestrator that coordinates all analysis steps:
1. Data extraction from documents
2. Structural validation
3. Similarity comparison
4. Financial capacity validation
5. Score calculation
6. Traffic light determination
7. Recommendation generation

### ExtractorCertificado
Extracts data from Chamber of Commerce certificates:
- NIT/Tax ID
- Company name
- Business object
- Assets and equity
- Legal representative
- Status (active/inactive)

### ComparadorTextos
Multi-algorithm text similarity comparator:
- Keyword matching (50% weight)
- N-gram similarity (20% weight)
- Sequence matching (10% weight)
- Jaccard index (10% weight)
- Important keywords boost (10% weight)

### ValidadorFinanciero
Validates financial capacity:
- Minimum 10% of process value in assets
- Scoring based on ratio
- Warnings and recommendations

## Configuration

### Pricing Configuration
Edit `pricing_config.py` to modify:
- Asset bands (A0-A3)
- Process value bands (V1-V5)
- Minimum prices
- Percentages
- Ceilings
- Social discount rules

### Analysis Configuration
Edit modules in `core/` to modify:
- Extraction patterns
- Similarity weights
- Validation rules
- Scoring formulas

## Deployment

### Production Settings
```bash
# Use production ASGI server
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Or use gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Environment Variables
```bash
# Optional configuration
export LICITIA_ENV=production
export LICITIA_LOG_LEVEL=info
```

## Support

For questions or issues:
- Check documentation: http://localhost:8000/docs
- Review test examples in `tests/`
- See usage examples in this guide

## Version History

**v2.0.0** (Current)
- ✅ Complete integration of analysis + pricing systems
- ✅ 98 comprehensive tests
- ✅ PDF file upload support
- ✅ Multi-algorithm similarity comparison
- ✅ WhatsApp message generation
- ✅ Dual pricing modes (enterprise/capped)

**v1.0.0** (Previous)
- ✅ Pricing calculator system
- ✅ 3-pillar monetization model
- ✅ REST API with FastAPI
