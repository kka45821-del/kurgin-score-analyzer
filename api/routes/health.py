from __future__ import annotations

from fastapi import APIRouter

from api.services.core_service import analyze_one, version_payload

router = APIRouter(tags=["health"])


@router.get("/health")
async def health():
    return {
        "status": "ok",
        "version": version_payload(),
    }


@router.get("/v1/health")
async def health_v1():
    return {
        "status": "ok",
        "version": version_payload(),
    }


@router.get("/v1/ready")
async def ready_v1():
    """Readiness check: import core and run a minimal one-stone analysis."""
    result = analyze_one({
        "Shape": "ROUND",
        "Report #": "READY-CHECK",
        "Lab": "KURGIN",
        "Weight": 1.00,
        "Measurements": "6.430x6.470x3.970",
        "CrownAngle": 34.5,
        "PavilionAngle": 40.8,
        "TablePercent": 56,
        "DepthPercent": 61.5,
        "CrownPercent": 15,
        "PavilionPercent": 43,
        "GirdlePercent": 3.5,
    })
    return {
        "status": "ready" if result.get("Calculation Status") == "OK" else "not_ready",
        "calculation_status": result.get("Calculation Status"),
        "version": version_payload(),
    }
