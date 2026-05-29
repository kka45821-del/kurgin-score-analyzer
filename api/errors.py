from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse


class KurginApiError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400, detail: dict | None = None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.detail = detail or {}


def error_payload(code: str, message: str, request_id: str = "", detail: dict | None = None):
    return {
        "status": "ERROR",
        "error": {
            "code": code,
            "message": message,
            "detail": detail or {},
            "request_id": request_id,
        },
    }


async def kurgin_api_error_handler(request: Request, exc: KurginApiError):
    request_id = getattr(request.state, "request_id", "")
    return JSONResponse(
        status_code=exc.status_code,
        content=error_payload(exc.code, exc.message, request_id=request_id, detail=exc.detail),
    )


async def generic_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", "")
    return JSONResponse(
        status_code=500,
        content=error_payload(
            "INTERNAL_ERROR",
            "Internal API error",
            request_id=request_id,
            detail={"type": exc.__class__.__name__},
        ),
    )
