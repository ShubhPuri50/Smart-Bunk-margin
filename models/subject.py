from core.attendance_calculator import (
    attendance_percent,
    safe_bunk_margin,
    recovery_classes,
)
from core.validators import validate_attendance
from core.risk_analyzer import classify_risk


class SubjectAttendance:
    def __init__(self, subject_name, attended, conducted, required_percentage):
        subject_name = str(subject_name).strip()
        if not subject_name:
            raise ValueError("subject name cannot be empty")
        validate_attendance(attended, conducted, required_percentage)
        self.subject_name = subject_name
        self.attended = attended
        self.conducted = conducted
        self.required_percentage = float(required_percentage)

    def calculate_percentage(self):
        return attendance_percent(self.attended, self.conducted)

    def calculate_bunk_margin(self):
        return safe_bunk_margin(
            self.attended, self.conducted, self.required_percentage
        )

    def calculate_recovery(self):
        return recovery_classes(
            self.attended, self.conducted, self.required_percentage
        )

    def classify_risk(self):
        return classify_risk(
            self.calculate_percentage(), self.required_percentage
        )
