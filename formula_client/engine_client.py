import os

from .cloud_client import calculate_stone_cloud
from .local_client import calculate_stone_local


def get_formula_mode():
    return os.getenv("FORMULA_MODE", "local").strip().lower()


def calculate_stone(engine_kwargs, mode=None):
    """Single calculation entry point for the site.

    mode='local': formula runs inside the app.
    mode='cloud': formula is requested from a closed API.
    mode='cloud_fallback': try cloud, fall back to local if cloud is unavailable.
    """
    selected_mode = (mode or get_formula_mode()).lower()

    if selected_mode == "cloud":
        return calculate_stone_cloud(engine_kwargs)
    if selected_mode == "cloud_fallback":
        try:
            return calculate_stone_cloud(engine_kwargs)
        except Exception:
            return calculate_stone_local(engine_kwargs)
    return calculate_stone_local(engine_kwargs)
