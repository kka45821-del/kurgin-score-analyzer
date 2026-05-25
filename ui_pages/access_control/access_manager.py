import json
from pathlib import Path

ACCESS_FILE = Path("access_settings.json")

ROLES = [
    "Guest",
    "Registered",
    "Jeweler",
    "Paid",
    "Professional",
    "Admin",
]

REPORT_LEVELS = [
    "Score Only",
    "Short Report",
    "Detailed Report",
    "Full Report",
    "Professional Report",
]

DEFAULT_ACCESS_MATRIX = {
    "Guest": ["Score Only"],
    "Registered": ["Score Only", "Short Report"],
    "Jeweler": ["Score Only", "Short Report", "Detailed Report"],
    "Paid": ["Score Only", "Short Report", "Detailed Report", "Full Report"],
    "Professional": ["Score Only", "Short Report", "Detailed Report", "Full Report", "Professional Report"],
    "Admin": REPORT_LEVELS,
}


def load_access_settings():
    if ACCESS_FILE.exists():
        try:
            return json.loads(ACCESS_FILE.read_text(encoding="utf-8"))
        except Exception:
            return DEFAULT_ACCESS_MATRIX.copy()
    return DEFAULT_ACCESS_MATRIX.copy()


def save_access_settings(settings):
    ACCESS_FILE.write_text(
        json.dumps(settings, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def get_allowed_levels(role, settings=None):
    settings = settings or load_access_settings()
    return settings.get(role, ["Score Only"])
