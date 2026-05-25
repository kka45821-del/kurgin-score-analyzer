from config_settings.engine_config import STRUCTURE_CONFIG


def clamp(x, low, high):
    return max(low, min(high, x))


def smooth_loss(x, dead=0.15, scale=0.70):
    z = max(0, x - dead) / scale
    return (z * z) / (1 + z * z)


def girdle_penalty_fn(girdle_pct):
    thick = smooth_loss((girdle_pct - 4.3) / 1.2, dead=0.05)
    thin = smooth_loss((1.2 - girdle_pct) / 0.8, dead=0.05)
    return 0.018 * thick + 0.022 * thin


def get_structure_modifier(
    crown_angle,
    pavilion_angle,
    table,
    depth,
    crown_pct,
    pavilion_pct,
    girdle_pct
):
    bd = (
        STRUCTURE_CONFIG["depth_base"]
        + STRUCTURE_CONFIG["depth_crown_coef"] * (crown_angle - 34.5)
        + STRUCTURE_CONFIG["depth_pavilion_coef"] * (pavilion_angle - 40.8)
        + STRUCTURE_CONFIG["depth_table_coef"] * (table - 56)
    )

    bc = (
        STRUCTURE_CONFIG["crown_base"]
        + STRUCTURE_CONFIG["crown_angle_coef"] * (crown_angle - 34.5)
        + STRUCTURE_CONFIG["crown_table_coef"] * (table - 56)
    )

    bp = (
        STRUCTURE_CONFIG["pavilion_base"]
        + STRUCTURE_CONFIG["pavilion_angle_coef"] * (pavilion_angle - 40.8)
    )

    depth_dev = max(0, abs(depth - bd) - STRUCTURE_CONFIG["depth_dead_zone"])
    crown_dev = max(0, abs(crown_pct - bc) - STRUCTURE_CONFIG["crown_dead_zone"])

    p_diff = pavilion_pct - bp
    p_asym = STRUCTURE_CONFIG["flat_pavilion_risk_multiplier"] if p_diff < 0 else 1.0
    pavilion_dev = max(
        0,
        abs(p_diff) * p_asym - STRUCTURE_CONFIG["pavilion_dead_zone"]
    )

    balance_err = max(
        0,
        abs(depth - (crown_pct + pavilion_pct + girdle_pct))
        - STRUCTURE_CONFIG["balance_dead_zone"]
    )

    g_penalty = girdle_penalty_fn(girdle_pct)

    total_loss = (
        STRUCTURE_CONFIG["pavilion_weight"] * smooth_loss(pavilion_dev)
        + STRUCTURE_CONFIG["depth_weight"] * smooth_loss(depth_dev)
        + STRUCTURE_CONFIG["crown_weight"] * smooth_loss(crown_dev)
        + STRUCTURE_CONFIG["balance_weight"] * smooth_loss(balance_err)
    )

    nailhead = 0
    if crown_angle > 35 and pavilion_angle > 41:
        nailhead = smooth_loss(
            (((crown_angle - 35.0) / 0.5) + ((pavilion_angle - 41.0) / 0.3)) / 2,
            dead=0.05
        )

    req_crown = 14.3 + max(0, table - 56) * 0.15
    fire_loss = smooth_loss(
        (max(0, req_crown - crown_pct) / 0.8)
        + (max(0, table - 59.0) / 1.5),
        dead=0.05
    )

    crit_pav = 39.6 + max(0, table - 58) * 0.20
    fisheye = 0
    if pavilion_angle < crit_pav:
        fisheye = smooth_loss(
            ((crit_pav - pavilion_angle) / 0.8)
            + (max(0, table - 59.5) / 2.0),
            dead=0.05
        )

    modifier = clamp(
        STRUCTURE_CONFIG["modifier_max"]
        - STRUCTURE_CONFIG["structure_loss_weight"] * total_loss
        - STRUCTURE_CONFIG["nailhead_penalty"] * nailhead
        - STRUCTURE_CONFIG["fisheye_penalty"] * fisheye
        - STRUCTURE_CONFIG["fire_penalty"] * fire_loss
        - g_penalty,
        STRUCTURE_CONFIG["modifier_min"],
        STRUCTURE_CONFIG["modifier_max"]
    )

    visual_check = (
        nailhead > STRUCTURE_CONFIG["visual_nailhead_threshold"]
        or fire_loss > STRUCTURE_CONFIG["visual_fire_threshold"]
        or fisheye > STRUCTURE_CONFIG["visual_fisheye_threshold"]
    )

    tags = []
    if modifier >= STRUCTURE_CONFIG["tag_perfect_modifier"]:
        tags.append("Perfect Build")
    if depth_dev > STRUCTURE_CONFIG["tag_hidden_weight_depth_dev"]:
        tags.append("Hidden Weight")
    if nailhead > STRUCTURE_CONFIG["tag_nailhead_threshold"]:
        tags.append("Nailhead Risk")
    if fisheye > STRUCTURE_CONFIG["tag_fisheye_threshold"]:
        tags.append("Fisheye Risk")
    if fire_loss > STRUCTURE_CONFIG["tag_fire_threshold"]:
        tags.append("Low Fire")

    return {
        "modifier": modifier,
        "tags": tags,
        "visual_check": visual_check,
        "diagnostics": {
            "nailhead": round(nailhead, 4),
            "fisheye": round(fisheye, 4),
            "fire_loss": round(fire_loss, 4),
            "depth_dev": round(depth_dev, 4),
            "crown_dev": round(crown_dev, 4),
            "pavilion_dev": round(pavilion_dev, 4),
            "balance_err": round(balance_err, 4),
            "girdle_penalty": round(g_penalty, 4),
            "ideal_depth": round(bd, 4),
            "ideal_crown": round(bc, 4),
            "ideal_pavilion": round(bp, 4),
            "total_loss": round(total_loss, 4)
        }
    }
