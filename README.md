# LicitIA - Hybrid Monetization Model API

## Overview

LicitIA implements a comprehensive 3-pillar hybrid monetization model for analyzing tender/bidding processes in Colombia. This API provides pricing calculations for different service tiers based on company assets and process values.

## 🎯 Architecture - 3 Pillars

### 1. **AVAILABILITY** (Monthly Subscription)
- WhatsApp chatbot access
- Micro-consultations and support
- Does NOT include complete tender analysis

### 2. **PAY PER PROCESS** (Transactional)
- **PLUS**: Quick validation (Chamber + RUT + fit assessment)
- **PRO**: Deep analysis (tenders + annexes + strategy)

### 3. **PREMIUM** (Custom Service)
- Case-by-case quotation
- Human service + AI assistance

---

## 💰 Pricing Model

### Monthly Subscription Plans

| Plan | Price/Month | Messages | Features |
|------|-------------|----------|----------|
| **POPULAR** | $19,900 | 30 | Short responses, document checklist, step-by-step guides |
| **PYME** | $49,900 | 120 | Everything above + process tracking + templates |
| **EMPRESA** | $129,900 | 400 | Everything above + priority + fast support |

**Anti-abuse rule**: Analysis of complete tenders/annexes → redirected to PRO per process

---

### PLUS - Quick Validation (Per Process)

**Formula**: `Price = MAX(MinimumByAssets, PercentageOfProcessValue)`

#### Asset Bands (A)

| Band | Range | Minimum Price |
|------|-------|---------------|
| **A0** | Not informed / $0 | $19,900 |
| **A1** | $1 – $200M | $29,900 |
| **A2** | $200M – $1,000M | $49,900 |
| **A3** | > $1,000M | $79,900 |

#### Process Value Bands (V)

| Band | Range | Percentage | Minimum |
|------|-------|------------|---------|
| **V1** | up to $50M | 0.08% | $19,900 |
| **V2** | $50M – $200M | 0.06% | — |
| **V3** | $200M – $800M | 0.05% | — |
| **V4** | $800M – $2,500M | 0.04% | — |
| **V5** | > $2,500M | 0.03% | — |

#### Example:
- Assets: $150M (A1) → Minimum $29,900
- Process value: $100M (V2) → 0.06% × $100M = $60,000
- **PLUS Price**: $60,000 (the higher of the two)

---

### PRO - Complete Analysis (Per Process)

**Formula**: `Price = MAX(MinimumByAssets, PercentageOfProcessValue) + AnnexesSurcharge`

**Ceiling**: $1,490,000 (higher amounts → PREMIUM quotation)

#### PRO Minimums by Assets

| Assets | Minimum |
|--------|---------|
| **A0** | $49,900 |
| **A1** | $79,900 |
| **A2** | $149,900 |
| **A3** | $249,900 |

#### PRO Percentage by Process Value

| Band | Percentage |
|------|------------|
| **V1** | 0.18% |
| **V2** | 0.14% |
| **V3** | 0.10% |
| **V4** | 0.08% |
| **V5** | 0.06% |

#### Annexes Surcharge

- **Included**: Up to 10 files
- **Additional**: $4,900 each
- **Package +10**: $39,900 for 10 files

#### Example:
- Assets: $500M (A2) → Minimum $149,900
- Process value: $300M (V3) → 0.10% × $300M = $300,000
- Files: 15 → +5 × $4,900 = $24,500
- **PRO Price**: $324,500

---

### 🎁 Social Discount (-30%)

Applies to PLUS and PRO if **ALL** criteria are met:

1. User type: `productor` / `economia_popular` / `asociacion`
2. Assets: A0 or A1 (≤ $200M)
3. Process value: V1 or V2 (≤ $200M)

**Anti-fraud**: Large companies pretending to be small → NO discount

---

### 📦 Package Discounts (PRO only)

| Quantity | Discount |
|----------|----------|
| 3 processes | 15% |
| 5+ processes | 25% |

---

## 🚀 API Endpoints

### Base URL
```
http://localhost:8000
```

### Health Check
```http
GET /api/pricing/health
```

**Response:**
```json
{
  "status": "ok",
  "service": "LicitIA Pricing API"
}
```

---

### Calculate PLUS Pricing
```http
POST /api/pricing/plus
```

**Request Body:**
```json
{
  "assets": 150000000,
  "process_value": 100000000,
  "user_type": "regular"
}
```

**Response:**
```json
{
  "service": "PLUS",
  "asset_band": "A1",
  "process_band": "V2",
  "minimum_by_assets": 29900,
  "percentage_based_price": 59999,
  "base_price": 59999,
  "discount_applied": false,
  "discount_amount": 0,
  "final_price": 59999,
  "breakdown": {
    "assets": 150000000,
    "process_value": 100000000,
    "user_type": "regular"
  }
}
```

---

### Calculate PRO Pricing
```http
POST /api/pricing/pro
```

**Request Body:**
```json
{
  "assets": 500000000,
  "process_value": 300000000,
  "num_annexes": 15,
  "user_type": "regular"
}
```

**Response:**
```json
{
  "service": "PRO",
  "asset_band": "A2",
  "process_band": "V3",
  "minimum_by_assets": 149900,
  "percentage_based_price": 300000,
  "base_price": 300000,
  "annexes_surcharge": 24500,
  "num_annexes": 15,
  "included_annexes": 10,
  "price_before_discount": 324500,
  "discount_applied": false,
  "discount_amount": 0,
  "final_price": 324500,
  "ceiling_exceeded": false,
  "ceiling_value": null,
  "breakdown": {
    "assets": 500000000,
    "process_value": 300000000,
    "user_type": "regular"
  }
}
```

---

### Calculate Package Discount
```http
POST /api/pricing/package
```

**Request Body:**
```json
{
  "base_price": 100000,
  "quantity": 5,
  "service": "PRO"
}
```

**Response:**
```json
{
  "service": "PRO",
  "quantity": 5,
  "price_per_process": 100000,
  "total_without_discount": 500000,
  "discount_percentage": 0.25,
  "discount_amount": 125000,
  "final_total": 375000,
  "price_per_process_after_discount": 75000
}
```

---

### Get Subscription Plans
```http
GET /api/pricing/subscription-plans
```

**Response:**
```json
{
  "POPULAR": {
    "price": 19900,
    "messages": 30,
    "features": [
      "Respuestas cortas",
      "Checklist documentos",
      "Guías paso a paso"
    ]
  },
  "PYME": {
    "price": 49900,
    "messages": 120,
    "features": [
      "Todo lo anterior",
      "Seguimiento procesos",
      "Plantillas"
    ]
  },
  "EMPRESA": {
    "price": 129900,
    "messages": 400,
    "features": [
      "Todo lo anterior",
      "Prioridad",
      "Soporte rápido"
    ]
  }
}
```

---

### Get Complete Quote
```http
POST /api/pricing/quote?include_subscription=true
```

**Request Body:**
```json
{
  "assets": 100000000,
  "process_value": 50000000,
  "num_annexes": 5,
  "user_type": "regular"
}
```

**Response:**
```json
{
  "plus": { ... },
  "pro": { ... },
  "recommendation": "PLUS",
  "subscription_plans": { ... }
}
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/danielojedameza-png/Licitia.git
cd Licitia
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
uvicorn main:app --reload
```

4. Access the API:
- API: `http://localhost:8000`
- Documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

---

## 🧪 Testing

Run all tests:
```bash
pytest
```

Run specific test files:
```bash
pytest test_pricing_calculator.py -v
pytest test_api.py -v
```

Run with coverage:
```bash
pytest --cov=. --cov-report=html
```

---

## 📊 Token/IA Call Limits (Cost Control)

| Service | AI Call Limit | Strategy |
|---------|---------------|----------|
| **Subscription** | 0 | Short responses, no large document analysis |
| **PLUS** | 1 | Reduced extracts (Chamber/RUT only) |
| **PRO** | 3 | Summary per file + hash-based cache |

**Smart Cache**: Re-uploaded files → served from cache

---

## 💬 WhatsApp Sales Flow (Post-DEMO)

### Positive DEMO ✅
```
🎯 DEMO Result: "YES you have a chance" ✅

Want to know exactly what you're missing to increase your score
and which documents could disqualify you?

1️⃣ PLUS (Chamber+RUT validation): $XX,XXX
2️⃣ PRO (tenders+annexes+strategy): $XX,XXX
3️⃣ WhatsApp monthly from $19,900 to accompany you

Which one do we start with?
```

### Negative DEMO ⚠️
```
⚠️ With what you have today, it's difficult to win.

But I can tell you EXACTLY what to fix
so you CAN compete.

PLUS Analysis: $XX,XXX
PRO Analysis: $XX,XXX

Interested?
```

---

## 📝 Request/Response Models

### User Types
- `regular`: Standard user (default)
- `productor`: Producer
- `economia_popular`: Popular economy
- `asociacion`: Association

### Service Types
- `PLUS`: Quick validation
- `PRO`: Complete analysis

### Asset Bands
- `A0`: Not informed / $0
- `A1`: $1 – $200M
- `A2`: $200M – $1,000M
- `A3`: > $1,000M

### Process Value Bands
- `V1`: up to $50M
- `V2`: $50M – $200M
- `V3`: $200M – $800M
- `V4`: $800M – $2,500M
- `V5`: > $2,500M

---

## 🔐 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- Browse all available endpoints
- See request/response schemas
- Test API calls directly from the browser

---

## 📄 License

This project is proprietary software for LicitIA/AGRODASIN.

---

## 👥 Contact

For questions or support, contact the AGRODASIN team.

---

## 🚦 Status

**Current Version**: 1.0.0  
**Status**: Production Ready ✅

---

## 📈 Next Steps

Potential enhancements:
1. WhatsApp integration (Twilio/360dialog)
2. Payment gateway integration (Wompi)
3. User authentication and authorization
4. Dashboard for metrics tracking
5. SECOP process alerts
6. Automated document analysis with AI
