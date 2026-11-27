import math
from .validators import validate_attendance


def attendance_percent(attended, conducted):
    if conducted < 0:
        raise ValueError("conducted classes cannot be negative")
    if attended < 0:
        raise ValueError("attended classes cannot be negative")
    if attended > conducted:
        raise ValueError("attended classes cannot exceed conducted classes")
    if conducted == 0:
        return 0.0
    return (attended / conducted) * 100


calculate_percentage = attendance_percent


def safe_bunk_margin(attended, conducted, required_pct):
    target = validate_attendance(attended, conducted, required_pct)
    ratio = target / 100
    if attendance_percent(attended, conducted) < target:
        return 0
    margin = math.floor((attended / ratio) - conducted + 1e-10)
    return max(0, margin)


def recovery_classes(attended, conducted, required_pct):
    target = validate_attendance(attended, conducted, required_pct)
    ratio = target / 100
    if attendance_percent(attended, conducted) >= target:
        return 0
    required = (ratio * conducted - attended) / (1 - ratio)
    return math.ceil(max(0, required) - 1e-10)
