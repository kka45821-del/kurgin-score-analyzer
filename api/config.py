from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List


def _split_csv(value: str | None) -> List[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class ApiSettings:
    api_version: str = "v1.12.3"
    service_name: str = "KURGIN Formula API"
    environment: str = os.getenv("KURGIN_API_ENV", "development")
    api_secret: str = os.getenv("KURGIN_API_SECRET", "")
    allowed_origins: List[str] = None
    default_language: str = os.getenv("KURGIN_DEFAULT_LANGUAGE", "RU")
    default_pdf_language: str = os.getenv("KURGIN_PDF_LANGUAGE", "BILINGUAL")
    max_batch_rows: int = int(os.getenv("KURGIN_MAX_BATCH_ROWS", "5000"))
    log_level: str = os.getenv("KURGIN_LOG_LEVEL", "INFO")
    require_secret_in_production: bool = os.getenv("KURGIN_REQUIRE_SECRET_IN_PROD", "true").lower() == "true"

    def __post_init__(self):
        object.__setattr__(
            self,
            "allowed_origins",
            _split_csv(os.getenv("KURGIN_ALLOWED_ORIGINS", "")) or ["*"],
        )

    @property
    def is_production(self) -> bool:
        return self.environment.lower() in {"prod", "production"}


def get_settings() -> ApiSettings:
    return ApiSettings()
