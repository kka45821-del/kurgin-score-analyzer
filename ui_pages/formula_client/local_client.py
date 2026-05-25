from core_formula.main_engine import get_final_diamond_analysis


def calculate_stone_local(engine_kwargs):
    """Local fallback calculation. Used until secure cloud formula API is enabled."""
    return get_final_diamond_analysis(**engine_kwargs)
