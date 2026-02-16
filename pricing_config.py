"""
Pricing Configuration for LicitIA Hybrid Monetization Model
Defines all pricing tiers, bands, and constants for the 3-pillar architecture:
1. Monthly Subscription (WhatsApp)
2. Pay Per Process (PLUS and PRO)
3. Premium (Custom quotes)
"""

from enum import Enum
from typing import Dict, Any


# Asset Bands (A0-A3)
class AssetBand(Enum):
    A0 = "A0"  # Not informed / $0
    A1 = "A1"  # $1 - $200M
    A2 = "A2"  # $200M - $1,000M
    A3 = "A3"  # > $1,000M


# Process Value Bands (V1-V5)
class ProcessValueBand(Enum):
    V1 = "V1"  # up to $50M
    V2 = "V2"  # $50M - $200M
    V3 = "V3"  # $200M - $800M
    V4 = "V4"  # $800M - $2,500M
    V5 = "V5"  # > $2,500M


# User Types for Social Discount
class UserType(Enum):
    PRODUCTOR = "productor"
    ECONOMIA_POPULAR = "economia_popular"
    ASOCIACION = "asociacion"
    REGULAR = "regular"


# Monthly Subscription Plans
SUBSCRIPTION_PLANS = {
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

# Asset Bands Thresholds (in COP)
ASSET_BAND_THRESHOLDS = {
    AssetBand.A0: (0, 0),  # Not informed
    AssetBand.A1: (1, 200_000_000),
    AssetBand.A2: (200_000_000, 1_000_000_000),
    AssetBand.A3: (1_000_000_000, float('inf'))
}

# Process Value Band Thresholds (in COP)
PROCESS_VALUE_BAND_THRESHOLDS = {
    ProcessValueBand.V1: (0, 50_000_000),
    ProcessValueBand.V2: (50_000_000, 200_000_000),
    ProcessValueBand.V3: (200_000_000, 800_000_000),
    ProcessValueBand.V4: (800_000_000, 2_500_000_000),
    ProcessValueBand.V5: (2_500_000_000, float('inf'))
}

# PLUS Pricing - Minimum by Assets
PLUS_MINIMUM_BY_ASSETS: Dict[AssetBand, int] = {
    AssetBand.A0: 19900,
    AssetBand.A1: 29900,
    AssetBand.A2: 49900,
    AssetBand.A3: 79900
}

# PLUS Pricing - Percentage by Process Value
PLUS_PERCENTAGE_BY_VALUE: Dict[ProcessValueBand, Dict[str, Any]] = {
    ProcessValueBand.V1: {"percentage": 0.0008, "minimum": 19900},
    ProcessValueBand.V2: {"percentage": 0.0006, "minimum": None},
    ProcessValueBand.V3: {"percentage": 0.0005, "minimum": None},
    ProcessValueBand.V4: {"percentage": 0.0004, "minimum": None},
    ProcessValueBand.V5: {"percentage": 0.0003, "minimum": None}
}

# PRO Pricing - Minimum by Assets
PRO_MINIMUM_BY_ASSETS: Dict[AssetBand, int] = {
    AssetBand.A0: 49900,
    AssetBand.A1: 79900,
    AssetBand.A2: 149900,
    AssetBand.A3: 249900
}

# PRO Pricing - Percentage by Process Value
PRO_PERCENTAGE_BY_VALUE: Dict[ProcessValueBand, float] = {
    ProcessValueBand.V1: 0.0018,
    ProcessValueBand.V2: 0.0014,
    ProcessValueBand.V3: 0.0010,
    ProcessValueBand.V4: 0.0008,
    ProcessValueBand.V5: 0.0006
}

# PRO Annexes Pricing
PRO_ANNEXES = {
    "included": 10,  # Up to 10 files included
    "additional_price": 4900,  # Per additional file
    "package_10_price": 39900,  # Package of +10 files
    "package_10_count": 10
}

# PRO Ceiling
PRO_CEILING = 1_490_000

# Social Discount
SOCIAL_DISCOUNT = {
    "percentage": 0.30,  # 30% discount
    "eligible_user_types": [
        UserType.PRODUCTOR,
        UserType.ECONOMIA_POPULAR,
        UserType.ASOCIACION
    ],
    "max_assets_band": AssetBand.A1,  # <= $200M
    "max_process_bands": [ProcessValueBand.V1, ProcessValueBand.V2]  # <= $200M
}

# Token/IA Call Limits
TOKEN_LIMITS = {
    "subscription": 0,  # No file analysis in subscription
    "plus": 1,  # 1 AI call
    "pro": 3  # 3 AI calls
}

# Package Discounts
PACKAGE_DISCOUNTS = {
    "pro_3_pack": {
        "quantity": 3,
        "discount": 0.15  # 15% discount
    },
    "pro_5_pack": {
        "quantity": 5,
        "discount": 0.25  # 25% discount
    }
}
