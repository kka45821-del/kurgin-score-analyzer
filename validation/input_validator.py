import math
from platform_config.app_config import SUPPORTED_SHAPES

REQUIRED_COLUMNS = ["CrownAngle","PavilionAngle","TablePercent","DepthPercent","CrownPercent","PavilionPercent","GirdlePercent"]
NUMERIC_COLUMNS = REQUIRED_COLUMNS
SOFT_LIMITS = {
    "CrownAngle": (20, 50),
    "PavilionAngle": (30, 50),
    "TablePercent": (40, 75),
    "DepthPercent": (45, 75),
    "CrownPercent": (5, 25),
    "PavilionPercent": (30, 55),
    "GirdlePercent": (0, 10),
}

def get_missing_columns(df):
    return [col for col in REQUIRED_COLUMNS if col not in df.columns]

def is_supported_shape(shape):
    return str(shape).upper() in SUPPORTED_SHAPES

def validate_numeric_value(value, column):
    try:
        number = float(value)
    except Exception:
        return False, f"{column}: not numeric"
    if math.isnan(number):
        return False, f"{column}: empty"
    if column in SOFT_LIMITS:
        low, high = SOFT_LIMITS[column]
        if not (low <= number <= high):
            return False, f"{column}: outside expected range {low}-{high}"
    return True, ""

def validate_row(row):
    errors = []
    for column in NUMERIC_COLUMNS:
        ok, message = validate_numeric_value(row.get(column), column)
        if not ok: errors.append(message)
    return errors
