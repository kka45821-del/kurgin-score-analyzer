from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from api.schemas import BatchJsonAnalyzeRequest, BatchJsonAnalyzeResponse, StoneAnalyzeRequest, StoneAnalyzeResponse
from api.security import require_api_key
from api.services.core_service import analyze_excel_bytes, analyze_one, analyze_rows, sanitize_record, summarize_dataframe, version_payload

router = APIRouter(prefix="/v1/analyze", tags=["analysis"], dependencies=[Depends(require_api_key)])


@router.post("/stone", response_model=StoneAnalyzeResponse)
async def analyze_stone_endpoint(payload: StoneAnalyzeRequest):
    try:
        result = analyze_one(payload.stone, language=payload.language)
        return {
            "status": result.get("Calculation Status", "OK"),
            "result": result,
            "version": version_payload(),
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/batch/json", response_model=BatchJsonAnalyzeResponse)
async def analyze_batch_json(payload: BatchJsonAnalyzeRequest):
    try:
        batch, summary, records = analyze_rows(payload.rows, language=payload.language)
        return {
            "status": "OK",
            **summary,
            "records": records if payload.include_records else None,
            "version": version_payload(),
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/batch/excel")
async def analyze_batch_excel(file: UploadFile = File(...), language: str = "RU", include_records: bool = True):
    try:
        data = await file.read()
        batch = analyze_excel_bytes(data, language=language)
        summary = summarize_dataframe(batch.dataframe)
        records = [sanitize_record(row) for row in batch.dataframe.to_dict(orient="records")] if include_records else None
        return {
            "status": "OK",
            **summary,
            "records": records,
            "version": version_payload(),
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
