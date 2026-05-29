from formula_client.local_client import calculate_stone_local
from config_settings.engine_config import ENGINE_VERSION


FORMULA_VERSION_ID = "current"
FORMULA_VERSION_NAME = "Current Local Formula"
FORMULA_VERSION_TYPE = "baseline"


def calculate(engine_kwargs):
    """Run current production/baseline local formula."""
    return calculate_stone_local(engine_kwargs)


def get_metadata():
    return {
        "version_id": FORMULA_VERSION_ID,
        "name": FORMULA_VERSION_NAME,
        "type": FORMULA_VERSION_TYPE,
        "engine_version": ENGINE_VERSION,
        "notes": "Baseline formula currently used by KURGIN Score Analyzer.",
    }
