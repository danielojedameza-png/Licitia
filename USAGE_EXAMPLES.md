# LicitIA Pricing API - Usage Examples

This document provides practical examples of using the LicitIA Pricing API.

## Starting the Server

```bash
# Install dependencies
pip install -r requirements.txt

# Start the development server
uvicorn main:app --reload

# Start the production server
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at:
- **Local**: http://localhost:8000
- **Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc

---

## Example 1: Calculate PLUS Pricing

### Scenario: Small company bidding on a medium-sized process

```bash
curl -X POST "http://localhost:8000/api/pricing/plus" \
  -H "Content-Type: application/json" \
  -d '{
    "assets": 150000000,
    "process_value": 100000000,
    "user_type": "regular"
  }'
```

**Response:**
```json
{
  "service": "PLUS",
  "asset_band": "A1",
  "process_band": "V2",
  "minimum_by_assets": 29900,
  "percentage_based_price": 60000,
  "base_price": 60000,
  "discount_applied": false,
  "discount_amount": 0,
  "final_price": 60000,
  "breakdown": {
    "assets": 150000000,
    "process_value": 100000000,
    "user_type": "regular"
  }
}
```

**Explanation**: The company has $150M in assets (A1 band) and is bidding on a $100M process (V2 band). The price is $60,000, which is 0.06% of the process value.

---

## Example 2: Calculate PRO Pricing with Annexes

### Scenario: Medium company with complex tender (15 documents)

```bash
curl -X POST "http://localhost:8000/api/pricing/pro" \
  -H "Content-Type: application/json" \
  -d '{
    "assets": 500000000,
    "process_value": 300000000,
    "num_annexes": 15,
    "user_type": "regular"
  }'
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

**Explanation**: Base price is $300,000 (0.10% of $300M). With 15 annexes, 10 are included and 5 extra cost $4,900 each ($24,500), totaling $324,500.

---

## Example 3: Social Discount Applied

### Scenario: Small producer bidding on a small process

```bash
curl -X POST "http://localhost:8000/api/pricing/plus" \
  -H "Content-Type: application/json" \
  -d '{
    "assets": 100000000,
    "process_value": 50000000,
    "user_type": "productor"
  }'
```

**Response:**
```json
{
  "service": "PLUS",
  "asset_band": "A1",
  "process_band": "V2",
  "minimum_by_assets": 29900,
  "percentage_based_price": 30000,
  "base_price": 30000,
  "discount_applied": true,
  "discount_amount": 9000,
  "final_price": 21000,
  "breakdown": {
    "assets": 100000000,
    "process_value": 50000000,
    "user_type": "productor"
  }
}
```

**Explanation**: As a producer with ≤$200M assets and ≤$200M process value, the user qualifies for a 30% social discount. Original price: $30,000. Discount: $9,000. Final: $21,000.

---

## Example 4: Package Discount for Multiple Processes

### Scenario: Company wants to analyze 5 processes

First, calculate individual PRO price:
```bash
curl -X POST "http://localhost:8000/api/pricing/pro" \
  -H "Content-Type: application/json" \
  -d '{
    "assets": 200000000,
    "process_value": 100000000,
    "num_annexes": 8
  }'
```

Then calculate package discount:
```bash
curl -X POST "http://localhost:8000/api/pricing/package" \
  -H "Content-Type: application/json" \
  -d '{
    "base_price": 140000,
    "quantity": 5,
    "service": "PRO"
  }'
```

**Response:**
```json
{
  "service": "PRO",
  "quantity": 5,
  "price_per_process": 140000,
  "total_without_discount": 700000,
  "discount_percentage": 0.25,
  "discount_amount": 175000,
  "final_total": 525000,
  "price_per_process_after_discount": 105000
}
```

**Explanation**: 5 processes at $140,000 each = $700,000. With 25% discount, you save $175,000, paying only $525,000 ($105,000 per process).

---

## Example 5: Get Complete Quote

### Scenario: Get all pricing options at once

```bash
curl -X POST "http://localhost:8000/api/pricing/quote" \
  -H "Content-Type: application/json" \
  -d '{
    "assets": 100000000,
    "process_value": 50000000,
    "num_annexes": 5,
    "user_type": "regular"
  }'
```

**Response:**
```json
{
  "plus": {
    "service": "PLUS",
    "final_price": 30000,
    ...
  },
  "pro": {
    "service": "PRO",
    "final_price": 79900,
    ...
  },
  "recommendation": "PLUS",
  "subscription_plans": {
    "POPULAR": {
      "price": 19900,
      "messages": 30,
      "features": [...]
    },
    ...
  }
}
```

**Explanation**: Get both PLUS and PRO quotes along with subscription options and a recommendation in a single call.

---

## Example 6: Get Subscription Plans

```bash
curl -X GET "http://localhost:8000/api/pricing/subscription-plans"
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

## Python Client Example

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000/api/pricing"

def get_plus_quote(assets, process_value, user_type="regular"):
    """Get PLUS pricing quote"""
    response = requests.post(
        f"{BASE_URL}/plus",
        json={
            "assets": assets,
            "process_value": process_value,
            "user_type": user_type
        }
    )
    return response.json()

def get_pro_quote(assets, process_value, num_annexes=0, user_type="regular"):
    """Get PRO pricing quote"""
    response = requests.post(
        f"{BASE_URL}/pro",
        json={
            "assets": assets,
            "process_value": process_value,
            "num_annexes": num_annexes,
            "user_type": user_type
        }
    )
    return response.json()

def get_complete_quote(assets, process_value, num_annexes=0):
    """Get complete pricing quote"""
    response = requests.post(
        f"{BASE_URL}/quote",
        json={
            "assets": assets,
            "process_value": process_value,
            "num_annexes": num_annexes
        }
    )
    return response.json()

# Example usage
if __name__ == "__main__":
    # Small producer
    quote = get_plus_quote(
        assets=100_000_000,
        process_value=50_000_000,
        user_type="productor"
    )
    print(f"PLUS price with social discount: ${quote['final_price']:,}")
    
    # Medium company with annexes
    quote = get_pro_quote(
        assets=500_000_000,
        process_value=300_000_000,
        num_annexes=15
    )
    print(f"PRO price with 15 annexes: ${quote['final_price']:,}")
```

---

## JavaScript/Node.js Client Example

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000/api/pricing';

async function getPlusQuote(assets, processValue, userType = 'regular') {
  const response = await axios.post(`${BASE_URL}/plus`, {
    assets: assets,
    process_value: processValue,
    user_type: userType
  });
  return response.data;
}

async function getProQuote(assets, processValue, numAnnexes = 0, userType = 'regular') {
  const response = await axios.post(`${BASE_URL}/pro`, {
    assets: assets,
    process_value: processValue,
    num_annexes: numAnnexes,
    user_type: userType
  });
  return response.data;
}

// Example usage
(async () => {
  // Small producer
  const plusQuote = await getPlusQuote(100000000, 50000000, 'productor');
  console.log(`PLUS price with social discount: $${plusQuote.final_price.toLocaleString()}`);
  
  // Medium company with annexes
  const proQuote = await getProQuote(500000000, 300000000, 15);
  console.log(`PRO price with 15 annexes: $${proQuote.final_price.toLocaleString()}`);
})();
```

---

## Error Handling

### Invalid Input Example

```bash
curl -X POST "http://localhost:8000/api/pricing/plus" \
  -H "Content-Type: application/json" \
  -d '{
    "assets": -100000000,
    "process_value": 50000000
  }'
```

**Response (422 Validation Error):**
```json
{
  "detail": [
    {
      "type": "greater_than_equal",
      "loc": ["body", "assets"],
      "msg": "Input should be greater than or equal to 0",
      "input": -100000000
    }
  ]
}
```

---

## Testing the API

Run all tests:
```bash
pytest -v
```

Run specific tests:
```bash
pytest test_pricing_calculator.py -v
pytest test_api.py::TestPlusEndpoint -v
```

---

## Health Check

```bash
curl http://localhost:8000/api/pricing/health
```

**Response:**
```json
{
  "status": "ok",
  "service": "LicitIA Pricing API"
}
```

---

## Interactive Documentation

Visit http://localhost:8000/docs in your browser to access the interactive Swagger UI where you can:
- See all available endpoints
- Test API calls directly
- View request/response schemas
- Download OpenAPI specification

---

For more information, see:
- **README.md**: Complete API documentation
- **IMPLEMENTATION_SUMMARY.md**: Technical implementation details
- **/docs**: Interactive API documentation
