ENGINE_VERSION = "Kurgin Round Engine v1.2-dev"


TRIPLE_CONFIG = {
    "target_crown": 34.5,
    "target_pavilion": 40.75,
    "target_table": 56,

    "crown_weight": 6,
    "pavilion_weight": 12,
    "table_weight": 2,

    "ideal_crown_min": 34.0,
    "ideal_crown_max": 35.0,

    "ideal_pavilion_min": 40.6,
    "ideal_pavilion_max": 40.9,

    "ideal_table_min": 54,
    "ideal_table_max": 58,

    "zone_bonus": 2,

    "steep_deep_crown_min": 35.0,
    "steep_deep_pavilion_min": 40.9,
    "steep_deep_penalty": 6,

    "shallow_crown_max": 34.0,
    "shallow_pavilion_max": 40.6,
    "shallow_penalty": 5,

    "large_table_threshold": 59,
    "large_table_weight": 2,

    "small_table_threshold": 53,
    "small_table_weight": 1.5,
}


STRUCTURE_CONFIG = {
    "modifier_min": 0.86,
    "modifier_max": 1.01,

    "depth_weight": 0.35,
    "crown_weight": 0.20,
    "pavilion_weight": 0.35,
    "balance_weight": 0.10,

    "structure_loss_weight": 0.12,
    "nailhead_penalty": 0.035,
    "fisheye_penalty": 0.020,
    "fire_penalty": 0.015,

    "depth_base": 61.5,
    "depth_crown_coef": 0.25,
    "depth_pavilion_coef": 0.35,
    "depth_table_coef": -0.10,

    "crown_base": 15.0,
    "crown_angle_coef": 0.14,
    "crown_table_coef": -0.04,

    "pavilion_base": 43.0,
    "pavilion_angle_coef": 0.18,

    "depth_dead_zone": 0.65,
    "crown_dead_zone": 0.60,
    "pavilion_dead_zone": 0.40,
    "balance_dead_zone": 0.35,

    "flat_pavilion_risk_multiplier": 1.15,

    "visual_nailhead_threshold": 0.10,
    "visual_fire_threshold": 0.15,
    "visual_fisheye_threshold": 0.10,

    "tag_perfect_modifier": 1.005,
    "tag_hidden_weight_depth_dev": 0.80,
    "tag_nailhead_threshold": 0.35,
    "tag_fisheye_threshold": 0.25,
    "tag_fire_threshold": 0.15,
}


FINAL_CONFIG = {
    "score_min": 0,
    "score_max": 100,

    "cap_threshold": 90.0,
    "cap_score": 89.9,

    "critical_nailhead_threshold": 0.35,
    "critical_fisheye_threshold": 0.30,

    "elite_threshold": 99,
    "top_threshold": 95,
    "high_threshold": 90,
    "standard_threshold": 80,

    "visual_check_threshold": 90,
}
