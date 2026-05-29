from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import get_settings
from api.errors import KurginApiError, generic_exception_handler, kurgin_api_error_handler
from api.middleware import RequestContextMiddleware
from api.routes import analyze, health, platform, reports
from api.security import validate_security_configuration


def create_app() -> FastAPI:
    settings = get_settings()
    validate_security_configuration()

    app = FastAPI(
        title="KURGIN Formula API",
        version=settings.api_version,
        description="Private API wrapper around KURGIN Score Analyzer Core SDK.",
    )

    app.add_middleware(RequestContextMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(KurginApiError, kurgin_api_error_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    app.include_router(health.router)
    app.include_router(analyze.router)
    app.include_router(reports.router)
    app.include_router(platform.router)
    return app


app = create_app()
