"""Compatibility entry point for the original project interface."""

from core.attendance_calculator import (
    attendance_percent,
    safe_bunk_margin,
    recovery_classes,
)
from core.validators import validate_attendance
from core.projection import projected_attendance
from core.risk_analyzer import risk_label
from storage.csv_manager import load_records, save_record
from services.attendance_service import analyze_attendance


def read_int(prompt, minimum=0):
    while True:
        try:
            value = int(input(prompt).strip())
            if value < minimum:
                print(f"Please enter a value >= {minimum}.")
                continue
            return value
        except ValueError:
            print("Input error: please enter a whole number.")


def read_float(prompt, minimum=0, maximum=100):
    import math
    while True:
        try:
            value = float(input(prompt).strip())
            if not math.isfinite(value) or not minimum <= value <= maximum:
                print(f"Please enter a value between {minimum} and {maximum}.")
                continue
            return value
        except ValueError:
            print("Input error: please enter a number.")


def read_subject():
    while True:
        subject = input("Subject: ").strip()
        if subject:
            return subject
        print("Subject name cannot be empty.")


def collect_attendance_inputs(include_future=False):
    subject = read_subject()
    conducted = read_int("Conducted classes: ", 1)
    while True:
        attended = read_int("Attended classes: ", 0)
        if attended <= conducted:
            break
        print("Attended classes cannot exceed conducted classes. Try again.")
    required = read_float("Required attendance (%): ", 1, 99)
    if include_future:
        upcoming = read_int("Upcoming classes: ", 0)
        while True:
            planned_bunks = read_int("Planned bunks: ", 0)
            if planned_bunks <= upcoming:
                break
            print("Planned bunks cannot exceed upcoming classes. Try again.")
        return subject, conducted, attended, required, upcoming, planned_bunks
    return subject, conducted, attended, required


def print_analysis(result):
    print("\n--- Attendance Defense Plan ---")
    print(f"Subject: {result['subject']}")
    print(f"Current attendance: {result['current']:.2f}%")
    print(f"Required attendance: {result['required']:.2f}%")
    print(f"Safe additional bunks: {result['margin']}")
    print(f"Recovery classes needed: {result['recovery']}")
    print(f"Projected attendance: {result['projection']:.2f}%")
    print(f"Status: {result['status']}")


def show_saved_records(filename="attendance_data.csv"):
    records = load_records(filename)
    print("\n--- Saved Attendance Records ---")
    if not records:
        print("No attendance records found.")
        return
    for index, record in enumerate(records, start=1):
        print(
            f"{index}. {record['subject']} | "
            f"Conducted: {record['conducted']} | "
            f"Attended: {record['attended']} | "
            f"Target: {record['required']}%"
        )


def run_self_tests():
    from main import run_tests
    return run_tests()


def main():
    from main import main as application_main
    application_main()


if __name__ == "__main__":
    main()
