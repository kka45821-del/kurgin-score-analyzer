from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from api.schemas import StoneAnalyzeRequest
from api.security import require_api_key
from api.services.core_service import version_payload
from api.services.platform_card_service import analyze_platform_card

router = APIRouter(prefix="/v1/platform", tags=["platform"], dependencies=[Depends(require_api_key)])


@router.post("/stone-card")
async def platform_stone_card(payload: StoneAnalyzeRequest, include_raw: bool = False, include_experimental: bool = True):
    try:
        response = analyze_platform_card(
            payload.stone,
            language=payload.language,
            include_raw=include_raw,
            include_experimental=include_experimental,
        )
        response["version"] = version_payload()
        return response
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
