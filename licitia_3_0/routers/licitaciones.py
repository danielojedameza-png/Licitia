"""
Router for licitaciones (tender/bidding) endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import Optional

# Create router
router = APIRouter(prefix="/api/licitaciones", tags=["licitaciones"])


@router.get("/health")
async def health_check():
    """Health check endpoint for licitaciones"""
    return {"status": "ok", "service": "LicitIA Licitaciones API"}


# Placeholder for future licitaciones endpoints
# This router can be expanded with specific tender/bidding functionality
