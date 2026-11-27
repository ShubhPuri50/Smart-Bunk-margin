import math


def validate_attendance(attended, conducted, required_pct):
    if not isinstance(conducted, int) or isinstance(conducted, bool):
        raise ValueError("conducted classes must be a whole number")
    if not isinstance(attended, int) or isinstance(attended, bool):
        raise ValueError("attended classes must be a whole number")
    if conducted < 1:
        raise ValueError("conducted classes must be at least 1")
    if attended < 0:
        raise ValueError("attended classes cannot be negative")
    if attended > conducted:
        raise ValueError("attended classes cannot exceed conducted classes")
    try:
        target = float(required_pct)
    except (TypeError, ValueError):
        raise ValueError("required attendance must be a number")
    if not math.isfinite(target) or not 1 <= target <= 99:
        raise ValueError("required attendance must be between 1% and 99%")
    return target
