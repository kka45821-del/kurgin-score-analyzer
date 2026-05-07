from config_settings.engine_config import ENGINE_VERSION, FINAL_CONFIG
from core_formula.triple_engine import get_triple_score
from core_formula.structure_engine import get_structure_modifier


def clamp(x, low, high):
    return max(low, min(high, x))


def get_final_diamond_analysis(
    crown_a,
    pav_a,
    table,
    depth,
    crown_p,
    pav_p,
    girdle_p
):
    triple = get_triple_score(crown_a, pav_a, table)

    struct = get_structure_modifier(
        crown_a,
        pav_a,
        table,
        depth,
        crown_p,
        pav_p,
        girdle_p
    )

    raw_final_score = triple * struct["modifier"]
    final_score = raw_final_score

    critical_risk = (
        struct["diagnostics"]["nailhead"] > FINAL_CONFIG["critical_nailhead_threshold"]
        or struct["diagnostics"]["fisheye"] > FINAL_CONFIG["critical_fisheye_threshold"]
    )

    cap_applied = False
    if final_score >= FINAL_CONFIG["cap_threshold"] and critical_risk:
        final_score = FINAL_CONFIG["cap_score"]
        cap_applied = True

    final_score = clamp(
        final_score,
        FINAL_CONFIG["score_min"],
        FINAL_CONFIG["score_max"]
    )

    if final_score >= FINAL_CONFIG["elite_threshold"]:
        verdict = "ELITE: Premium Build"
    elif final_score >= FINAL_CONFIG["top_threshold"]:
        verdict = "TOP: Excellent Selection"
    elif final_score >= FINAL_CONFIG["high_threshold"]:
        verdict = "HIGH: Great Quality"
    elif final_score >= FINAL_CONFIG["standard_threshold"]:
        verdict = "STD: Commercial Grade"
    else:
        verdict = "REJECT: Poor Performance"

    if critical_risk and final_score >= FINAL_CONFIG["standard_threshold"]:
        verdict = "CAUTION: Critical Optical Risk"
    elif critical_risk:
        verdict = "REJECT: Poor Performance"
    elif struct["visual_check"] and final_score >= FINAL_CONFIG["visual_check_threshold"]:
        verdict = "NOTICE: Visual Check Recommended"

    breakdown = f"""
ENGINE
Version: {ENGINE_VERSION}

TRIPLE
Triple Score: {round(triple, 2)}

INPUT PARAMETERS
Crown Angle: {crown_a}
Pavilion Angle: {pav_a}
Table %: {table}
Depth %: {depth}
Crown %: {crown_p}
Pavilion %: {pav_p}
Girdle %: {girdle_p}

STRUCTURE
Structure Modifier: {round(struct["modifier"], 4)}

IDEAL STRUCTURE TARGETS
Ideal Depth: {struct["diagnostics"]["ideal_depth"]}
Ideal Crown %: {struct["diagnostics"]["ideal_crown"]}
Ideal Pavilion %: {struct["diagnostics"]["ideal_pavilion"]}

DIAGNOSTICS
Total Loss: {struct["diagnostics"]["total_loss"]}
Nailhead: {struct["diagnostics"]["nailhead"]}
Fisheye: {struct["diagnostics"]["fisheye"]}
Fire Loss: {struct["diagnostics"]["fire_loss"]}
Depth Dev: {struct["diagnostics"]["depth_dev"]}
Crown Dev: {struct["diagnostics"]["crown_dev"]}
Pavilion Dev: {struct["diagnostics"]["pavilion_dev"]}
Balance Err: {struct["diagnostics"]["balance_err"]}
Girdle Penalty: {struct["diagnostics"]["girdle_penalty"]}

FLAGS
Visual Check: {struct["visual_check"]}
Critical Risk: {critical_risk}
Cap Applied: {cap_applied}

FINAL
Raw Final Score: {round(raw_final_score, 2)}
Final Score: {round(final_score, 2)}
Verdict: {verdict}
"""

    return {
        "engine_version": ENGINE_VERSION,
        "final_score": round(final_score, 2),
        "final_verdict": verdict,
        "triple_score": round(triple, 2),
        "structure_modifier": round(struct["modifier"], 4),
        "structure_tags": struct["tags"],
        "visual_check": struct["visual_check"],
        "critical_risk": critical_risk,
        "diagnostics": struct["diagnostics"],
        "breakdown": breakdown
    }
