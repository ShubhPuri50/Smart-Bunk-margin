from core.attendance_calculator import (
    attendance_percent,
    safe_bunk_margin,
    recovery_classes,
)
from core.projection import projected_attendance
from core.risk_analyzer import classify_risk
from core.validators import validate_attendance


def analyze_attendance(subject, conducted, attended, required,
                       upcoming=0, planned_bunks=0):
    subject = str(subject).strip()
    if not subject:
        raise ValueError("subject name cannot be empty")
    validate_attendance(attended, conducted, required)
    if upcoming < 0 or planned_bunks < 0 or planned_bunks > upcoming:
        raise ValueError("planned bunks must be between 0 and upcoming classes")
    current = attendance_percent(attended, conducted)
    projection = projected_attendance(attended, conducted, upcoming, planned_bunks)
    if upcoming == 0:
        projection = current
    return {
        "subject": subject,
        "current": current,
        "required": float(required),
        "margin": safe_bunk_margin(attended, conducted, required),
        "recovery": recovery_classes(attended, conducted, required),
        "upcoming": upcoming,
        "planned_bunks": planned_bunks,
        "projection": projection,
        "status": classify_risk(current, float(required)),
    }
