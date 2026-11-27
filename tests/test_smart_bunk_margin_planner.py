import unittest
import tempfile
import os
from smart_bunk_margin_planner import (
    attendance_percent, validate_attendance, safe_bunk_margin,
    recovery_classes, projected_attendance, risk_label,
    analyze_attendance, save_record, load_records
)
from core.projection import check_future_plan
from storage.csv_manager import upsert_record, create_subject_index
from services.report_service import (
    calculate_statistics,
    generate_insights,
    generate_subject_summary,
)
from models.student import Student
from models.subject import SubjectAttendance
from models.attendance_planner import AttendancePlanner
from models.report import AttendanceReport, BaseReport

class AttendancePlannerTests(unittest.TestCase):
    def test_attendance_percentage(self):
        self.assertAlmostEqual(attendance_percent(19, 24), 79.1666667, places=5)

    def test_bunk_margin(self):
        self.assertEqual(safe_bunk_margin(19, 24, 75), 1)

    def test_recovery_classes(self):
        self.assertEqual(recovery_classes(20, 30, 75), 10)

    def test_exact_target_boundary(self):
        self.assertEqual(safe_bunk_margin(3, 4, 75), 0)

    def test_below_target_margin_zero(self):
        self.assertEqual(safe_bunk_margin(20, 30, 75), 0)

    def test_future_projection(self):
        self.assertAlmostEqual(projected_attendance(19, 24, 6, 1), 80.0)

    def test_risk_below_target(self):
        self.assertEqual(risk_label(70, 75), "BELOW TARGET")

    def test_risk_watch(self):
        self.assertEqual(risk_label(79, 75), "WATCH")

    def test_risk_safe(self):
        self.assertEqual(risk_label(80, 75), "SAFE")

    def test_invalid_conducted(self):
        with self.assertRaises(ValueError):
            validate_attendance(5, 0, 75)

    def test_attended_exceeds_conducted(self):
        with self.assertRaises(ValueError):
            validate_attendance(11, 10, 75)

    def test_invalid_target(self):
        with self.assertRaises(ValueError):
            validate_attendance(8, 10, 100)

    def test_bunks_exceed_upcoming(self):
        with self.assertRaises(ValueError):
            projected_attendance(10, 20, 3, 4)

    def test_blank_subject(self):
        with self.assertRaises(ValueError):
            analyze_attendance("  ", 10, 8, 75)

    def test_csv_round_trip(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "attendance.csv")
            save_record("Test Subject", 10, 8, 75, path)
            rows = load_records(path)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["subject"], "Test Subject")

    def test_watch_and_safe_boundaries(self):
        self.assertEqual(risk_label(75, 75), "WATCH")
        self.assertEqual(risk_label(80, 75), "SAFE")

    def test_future_plan_acceptability(self):
        self.assertEqual(check_future_plan(19, 24, 6, 1, 75), "PLAN ACCEPTABLE")
        self.assertEqual(check_future_plan(19, 24, 6, 6, 75), "PLAN NOT SAFE")
        self.assertEqual(check_future_plan(19, 24, 3, 4, 75), "INVALID PLAN")

    def test_subject_lookup_dictionary(self):
        records = [{"subject": "Physics", "conducted": 28, "attended": 22,
                    "required": 75}]
        index = create_subject_index(records)
        self.assertEqual(index["physics"]["attended"], 22)
        self.assertIsNone(index.get("chemistry"))

    def test_duplicate_subject_is_updated(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "attendance.csv")
            upsert_record("Physics", 20, 15, 75, path)
            upsert_record("Physics", 22, 18, 75, path)
            rows = load_records(path)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["attended"], 18)

    def test_oop_composition_and_methods(self):
        student = Student("S1", "Test Student")
        planner = AttendancePlanner(student)
        record = planner.add_subject("Physics", 22, 28, 75)
        self.assertAlmostEqual(record.calculate_percentage(), 78.5714286, places=5)
        self.assertEqual(record.classify_risk(), "WATCH")
        self.assertIs(planner.analyze_subject("physics"), record)

    def test_report_inheritance_and_statistics(self):
        records = [
            {"subject": "Physics", "conducted": 28, "attended": 22, "required": 75},
            {"subject": "Mathematics", "conducted": 30, "attended": 25, "required": 75},
        ]
        stats = calculate_statistics(records)
        self.assertEqual(stats["subjects"], 2)
        self.assertEqual(stats["safe"], 1)
        report = AttendanceReport("Attendance Report", [
            {**row, "_percentage": 80.0, "_risk": "SAFE"}
            for row in generate_subject_summary(records)
        ])
        self.assertIn("Attendance Report", report.generate_header())
        self.assertIn("Physics", report.generate_summary())
        self.assertTrue(generate_insights(records))

if __name__ == "__main__":
    unittest.main(verbosity=2)
