from config_settings.engine_config import TRIPLE_CONFIG


def clamp(x, low, high):
    return max(low, min(high, x))


def get_triple_score(crown_angle, pavilion_angle, table):
    angle_base = (
        100
        - abs(crown_angle - TRIPLE_CONFIG["target_crown"]) * TRIPLE_CONFIG["crown_weight"]
        - abs(pavilion_angle - TRIPLE_CONFIG["target_pavilion"]) * TRIPLE_CONFIG["pavilion_weight"]
        - abs(table - TRIPLE_CONFIG["target_table"]) * TRIPLE_CONFIG["table_weight"]
    )

    zone_bonus = TRIPLE_CONFIG["zone_bonus"] if (
        TRIPLE_CONFIG["ideal_crown_min"] <= crown_angle <= TRIPLE_CONFIG["ideal_crown_max"]
        and TRIPLE_CONFIG["ideal_pavilion_min"] <= pavilion_angle <= TRIPLE_CONFIG["ideal_pavilion_max"]
        and TRIPLE_CONFIG["ideal_table_min"] <= table <= TRIPLE_CONFIG["ideal_table_max"]
    ) else 0

    combo_penalty = 0

    if (
        crown_angle > TRIPLE_CONFIG["steep_deep_crown_min"]
        and pavilion_angle > TRIPLE_CONFIG["steep_deep_pavilion_min"]
    ):
        combo_penalty += TRIPLE_CONFIG["steep_deep_penalty"]

    if (
        crown_angle < TRIPLE_CONFIG["shallow_crown_max"]
        and pavilion_angle < TRIPLE_CONFIG["shallow_pavilion_max"]
    ):
        combo_penalty += TRIPLE_CONFIG["shallow_penalty"]

    if table > TRIPLE_CONFIG["large_table_threshold"]:
        combo_penalty += (
            table - TRIPLE_CONFIG["large_table_threshold"]
        ) * TRIPLE_CONFIG["large_table_weight"]

    if table < TRIPLE_CONFIG["small_table_threshold"]:
        combo_penalty += (
            TRIPLE_CONFIG["small_table_threshold"] - table
        ) * TRIPLE_CONFIG["small_table_weight"]

    return clamp(angle_base + zone_bonus - combo_penalty, 0, 100)
