from __future__ import annotations

from fastapi import Header, HTTPException, status

from api.config import get_settings


def validate_security_configuration():
    settings = get_settings()
    if settings.is_production and settings.require_secret_in_production and not settings.api_secret:
        raise RuntimeError("KURGIN_API_SECRET must be set in production")


async def require_api_key(x_kurgin_api_key: str | None = Header(default=None)):
    """API-key boundary.

    Development: if KURGIN_API_SECRET is empty, requests are allowed.
    Production: KURGIN_API_SECRET is required by startup validation.
    """
    settings = get_settings()
    if not settings.api_secret:
        return True

    if not x_kurgin_api_key or x_kurgin_api_key != settings.api_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing KURGIN API key",
        )
    return True
