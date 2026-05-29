from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class StoneAnalyzeRequest(BaseModel):
    language: str = Field(default="RU", description="RU or EN localization for generated text")
    stone: Dict[str, Any] = Field(..., description="Stone parameters using KURGIN canonical fields or aliases")


class StoneAnalyzeResponse(BaseModel):
    status: str
    result: Dict[str, Any]
    version: Dict[str, Any]


class BatchJsonAnalyzeRequest(BaseModel):
    language: str = Field(default="RU")
    rows: List[Dict[str, Any]]
    include_records: bool = Field(default=True)


class BatchJsonAnalyzeResponse(BaseModel):
    status: str
    rows_total: int
    rows_ok: int
    rows_issues: int
    records: Optional[List[Dict[str, Any]]] = None
    version: Dict[str, Any]


class PdfExportRequest(BaseModel):
    language: str = Field(default="BILINGUAL")
    stone_result: Dict[str, Any]


class ErrorResponse(BaseModel):
    detail: str
