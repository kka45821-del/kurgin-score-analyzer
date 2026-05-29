from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile

from api.schemas import PdfExportRequest
from api.security import require_api_key
from api.services.core_service import export_batch_excel, export_batch_package, export_stone_pdf

router = APIRouter(prefix="/v1/export", tags=["exports"], dependencies=[Depends(require_api_key)])


@router.post("/stone/pdf")
async def export_stone_pdf_endpoint(payload: PdfExportRequest):
    try:
        pdf = export_stone_pdf(payload.stone_result, language=payload.language)
        return Response(
            content=pdf,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=kurgin_stone_report.pdf"},
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/batch/excel")
async def export_batch_excel_endpoint(file: UploadFile = File(...), language: str = "RU"):
    try:
        data = await file.read()
        output = export_batch_excel(data, language=language)
        return Response(
            content=output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=kurgin_score_result.xlsx"},
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/batch/package")
async def export_batch_package_endpoint(file: UploadFile = File(...), language: str = "RU", pdf_mode: str = "all_ok"):
    try:
        data = await file.read()
        output = export_batch_package(data, language=language, pdf_mode=pdf_mode)
        return Response(
            content=output,
            media_type="application/zip",
            headers={"Content-Disposition": "attachment; filename=kurgin_analysis_package.zip"},
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
