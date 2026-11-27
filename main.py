import math
import unittest

from config import DATA_FILE
from core.attendance_calculator import (
    attendance_percent,
    safe_bunk_margin,
    recovery_classes,
)
from core.projection import projected_attendance
from core.risk_analyzer import classify_risk
from core.validators import validate_attendance
from models.student import Student
from storage.csv_manager import load_records, upsert_record, create_subject_index
from services.attendance_service import analyze_attendance
from services.report_service import (
    generate_subject_summary,
    calculate_statistics,
    generate_insights,
)
from models.report import AttendanceReport
from visualization.charts import generate_charts


def read_int(prompt, minimum=0, maximum=None):
    while True:
        try:
            value = int(input(prompt).strip())
            if value < minimum or (maximum is not None and value > maximum):
                raise ValueError
            return value
        except ValueError:
            print("Input error: enter a valid whole number.")


def read_float(prompt, minimum=1, maximum=99):
    while True:
        try:
            value = float(input(prompt).strip())
            if not math.isfinite(value) or not minimum <= value <= maximum:
                raise ValueError
            return value
        except ValueError:
            print(f"Please enter a number between {minimum} and {maximum}.")


def read_attendance(include_future=False):
    subject = input("Subject: ").strip()
    if not subject:
        raise ValueError("subject name cannot be empty")
    conducted = read_int("Conducted classes: ", 1)
    attended = read_int("Attended classes: ", 0)
    required = read_float("Required attendance (%): ")
    validate_attendance(attended, conducted, required)
    if include_future:
        upcoming = read_int("Upcoming classes: ", 0)
        planned = read_int("Planned bunks: ", 0, upcoming)
        return subject, conducted, attended, required, upcoming, planned
    return subject, conducted, attended, required


def print_summary(records):
    rows = generate_subject_summary(records)
    print("\nSubject-wise Attendance Summary")
    print("Subject | Attended/Conducted | Percentage | Risk")
    for row in rows:
        print(
            f"{row['subject']} | {row['attended']}/{row['conducted']} "
            f"| {row['_percentage']:.2f}% | {row['_risk']}"
        )
    if not rows:
        print("No attendance records found.")
        return
    stats = calculate_statistics(records)
    print("\nStatistics")
    print(f"Total subjects: {stats['subjects']}")
    print(f"Total classes attended: {stats['attended']}")
    print(f"Total classes conducted: {stats['conducted']}")
    print(f"Average subject-wise attendance: {stats['average']:.2f}%")
    print(f"Combined attendance: {stats['combined']:.2f}%")
    print(f"Highest: {stats['highest']['subject']} ({stats['highest']['_percentage']:.2f}%)")
    print(f"Lowest: {stats['lowest']['subject']} ({stats['lowest']['_percentage']:.2f}%)")
    print(f"BELOW TARGET: {stats['below']} | WATCH: {stats['watch']} | SAFE: {stats['safe']}")


def run_tests():
    suite = unittest.defaultTestLoader.loadTestsFromName(
        "tests.test_smart_bunk_margin_planner"
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return result.wasSuccessful()


def main():
    student = Student("S26CSEU3581", "Shubh Puri")
    print("\nSMART BUNK MARGIN & ATTENDANCE PLANNER")
    while True:
        print("\n1. Create Student Profile")
        print("2. Add Subject Attendance")
        print("3. View Subject Attendance")
        print("4. Calculate Attendance Percentage")
        print("5. Calculate Safe Bunk Margin")
        print("6. Calculate Recovery Classes")
        print("7. Project Future Attendance")
        print("8. Analyze Attendance Risk")
        print("9. Generate Attendance Summary")
        print("10. View Attendance Charts")
        print("11. Generate Attendance Insights")
        print("12. Run System Tests")
        print("13. Exit")
        choice = input("Enter your choice: ").strip()
        try:
            if choice == "1":
                student_id = input("Student ID: ").strip()
                name = input("Student name: ").strip()
                student = Student(student_id, name)
                print("Student profile created.")
            elif choice in {"2", "4", "5", "6", "7", "8"}:
                values = read_attendance(include_future=choice == "7")
                if choice == "2":
                    upsert_record(values[0], values[1], values[2], values[3])
                    print("Subject attendance saved or updated.")
                else:
                    if choice == "7":
                        subject, conducted, attended, required, upcoming, planned = values
                        result = analyze_attendance(
                            subject, conducted, attended, required, upcoming, planned
                        )
                        print(f"Projected attendance: {result['projection']:.2f}%")
                    else:
                        subject, conducted, attended, required = values
                        if choice == "4":
                            print(f"Attendance: {attendance_percent(attended, conducted):.2f}%")
                        elif choice == "5":
                            print(f"Safe bunks: {safe_bunk_margin(attended, conducted, required)}")
                        elif choice == "6":
                            print(f"Recovery classes: {recovery_classes(attended, conducted, required)}")
                        elif choice == "8":
                            print(f"Status: {classify_risk(attendance_percent(attended, conducted), required)}")
            elif choice == "3":
                records = load_records(DATA_FILE)
                index = create_subject_index(records)
                if not records:
                    print("No attendance records found.")
                else:
                    subject = input("Subject (leave blank for all): ").strip()
                    selected = [index[subject.lower()]] if subject else records
                    if subject and subject.lower() not in index:
                        print("Subject not found.")
                    else:
                        for record in selected:
                            print(
                                f"{record['subject']} | Conducted: {record['conducted']} "
                                f"| Attended: {record['attended']} "
                                f"| Target: {record['required']}%"
                            )
            elif choice == "9":
                print_summary(load_records(DATA_FILE))
            elif choice == "10":
                paths = generate_charts(load_records(DATA_FILE))
                if paths:
                    print("Charts saved:")
                    for path in paths:
                        print(path)
                else:
                    print("No records available to chart.")
            elif choice == "11":
                insights = generate_insights(load_records(DATA_FILE))
                print("\nATTENDANCE INSIGHTS")
                for insight in insights:
                    print("- " + insight)
            elif choice == "12":
                run_tests()
            elif choice == "13":
                print("Planner closed.")
                break
            else:
                print("Invalid menu choice.")
        except ValueError as error:
            print(f"Input error: {error}")


if __name__ == "__main__":
    main()
