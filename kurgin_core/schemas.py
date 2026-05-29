"""Lightweight schema notes for KURGIN Platform integration.

This module intentionally avoids hard dependencies such as pydantic.
The Selectel/backend API can later formalize these schemas in FastAPI/Pydantic.
"""

STONE_INPUT_MINIMUM = {
    "Shape": "ROUND",
    "CrownAngle": 34.5,
    "PavilionAngle": 40.8,
    "TablePercent": 56.0,
    "DepthPercent": 61.5,
    "CrownPercent": 15.0,
    "PavilionPercent": 43.0,
    "GirdlePercent": 3.5,
}

STONE_IDENTITY_OPTIONAL = {
    "Stock #": "supplier stock id",
    "Report #": "lab report number",
    "Lab": "IGI/GIA/etc",
    "Weight": "carat weight",
    "Color": "color grade",
    "Clarity": "clarity grade",
    "Measurements": "6.430x6.470x3.970",
}

CORE_OUTPUT_KEYS = [
    "Kurgin Score",
    "Verdict",
    "Verdict Local",
    "score_band_label_ru",
    "tags_all",
    "tag1",
    "tag2",
    "tag3",
    "tag4",
    "tag5",
    "tag6",
    "interpretation_short_ru",
    "recommendation_ru",
    "warning_ru",
    "Calculation Status",
]
